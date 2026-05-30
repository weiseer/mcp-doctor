#!/usr/bin/env python3
"""
weiseer mcp-doctor — scanner core v0.2.0 (Day 2)

Day 2 changes vs v0.1.0:
- A1 calibration: ^/~ only -3 (was -8), `*`/`latest` separate harder signal
- C1/C2/C3 REAL: OSV API integration (osv.dev) for CVE lookup
- B4 NEW: GitHub last-push-staleness via GitHub API
- Typosquat: short-name tokenization (catches mcp-server-X vs server-X)
- Self-disclosure flag for known-weiseer packages

Open-source rubric at rubric.yaml. CLI wrapper in Node.js to come (Day 3).
Apache-2.0. Probe ID: P-010.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("error: pyyaml required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

RUBRIC_PATH = Path(__file__).parent / "rubric.yaml"
TIMEOUT = 12
USER_AGENT = "weiseer-mcp-doctor/0.2.0"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

OFFICIAL_MCP_PREFIXES = [
    "@modelcontextprotocol/",
    "@anthropic-ai/",
    "@anthropic/",
    "@openai/",
    "@cloudflare/",
]

# Short-name tokens for typosquat detection.
# Pattern: official package "server-X" → suspicious if community packages
# name themselves "mcp-server-X" / "X-mcp" / etc. with very close token overlap.
OFFICIAL_SHORT_NAMES = [
    "sdk", "server-github", "server-filesystem", "server-postgres",
    "server-slack", "server-gdrive", "server-puppeteer", "server-fetch",
    "server-memory", "server-time", "server-sequential-thinking",
]

# Known organism brand for self-disclosure flag (PASS but with note)
SELF_DISCLOSURE_PREFIXES = ["@weiseer/"]


@dataclass
class TriggeredSignal:
    signal_id: str
    deduct: int
    hard_block: bool
    evidence: str
    rationale: str


@dataclass
class ScanResult:
    package: str
    version: str
    verdict: str
    score: int
    self_disclosure: bool = False
    triggered_signals: list[TriggeredSignal] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    scanned_at: str = ""
    rubric_version: str = ""
    error: str | None = None


# ---- HTTP helpers ----

def http_json(url: str, method: str = "GET", body: dict | None = None, headers: dict | None = None) -> Any:
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def http_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


# ---- text helpers ----

def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = curr
    return prev[-1]


def short_name(pkg: str) -> str:
    """Strip scope, strip 'mcp-' prefix, strip '-mcp' suffix → core token."""
    n = pkg.split("/")[-1].lower()
    for prefix in ("mcp-",):
        if n.startswith(prefix):
            n = n[len(prefix):]
    for suffix in ("-mcp", "-server"):
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    return n


def detect_typosquat(name: str) -> tuple[bool, str]:
    """Detect by both full-name and short-name comparison."""
    if any(name.startswith(p) for p in OFFICIAL_MCP_PREFIXES):
        return False, ""  # official itself
    sn = short_name(name)
    for official in OFFICIAL_SHORT_NAMES:
        os_short = short_name(official)
        if not os_short:
            continue
        if sn == os_short:
            return True, f"short-name exact match with official '{official}'"
        if len(sn) >= 4 and edit_distance(sn, os_short) <= 1:
            return True, f"short-name within edit-distance 1 of official '{official}' (you={sn}, them={os_short})"
    return False, ""


# ---- npm + tarball ----

def fetch_npm_metadata(pkg: str) -> dict:
    encoded = urllib.parse.quote(pkg, safe="@/")
    return http_json(f"https://registry.npmjs.org/{encoded}")


def fetch_tarball_inspect(tarball_url: str) -> dict:
    raw = http_bytes(tarball_url)
    out = {"package_json": None, "files": [], "scripts": {}, "src_concat": ""}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            name = member.name
            rel = name[len("package/"):] if name.startswith("package/") else name
            out["files"].append(rel)
            if rel == "package.json":
                try:
                    f = tar.extractfile(member)
                    if f:
                        pj = json.loads(f.read().decode("utf-8", errors="replace"))
                        out["package_json"] = pj
                        out["scripts"] = pj.get("scripts", {}) or {}
                except Exception:
                    pass
            elif rel.endswith((".js", ".mjs", ".cjs", ".ts")) and len(out["src_concat"]) < 200_000:
                try:
                    f = tar.extractfile(member)
                    if f:
                        out["src_concat"] += f.read(50_000).decode("utf-8", errors="replace") + "\n"
                except Exception:
                    pass
    return out


# ---- OSV CVE lookup (Day 2 NEW — direct upstream) ----

def osv_vulns_for_package(pkg: str, version: str | None = None) -> list[dict]:
    """Returns list of OSV vuln records for an npm package."""
    body: dict[str, Any] = {"package": {"ecosystem": "npm", "name": pkg}}
    if version:
        body["version"] = version
    try:
        resp = http_json("https://api.osv.dev/v1/query", method="POST", body=body)
        return resp.get("vulns") or []
    except Exception:
        return []


def osv_severity(vuln: dict) -> str:
    """Best-effort severity classification."""
    sev = vuln.get("severity") or []
    for s in sev:
        ssc = s.get("score") or ""
        if "CRITICAL" in ssc.upper():
            return "CRITICAL"
        # CVSS string like "CVSS:3.1/AV:N/...". Map numeric to bucket if present.
    db_specific = vuln.get("database_specific") or {}
    sev_str = (db_specific.get("severity") or "").upper()
    if sev_str:
        return sev_str
    aliases = vuln.get("aliases") or []
    if any("GHSA" in a for a in aliases):
        return "HIGH"
    return "MEDIUM"


# ---- GitHub last-push lookup (Day 2 NEW) ----

GH_REPO_RE = re.compile(r"github\.com[:/]+([^/]+)/([^/.\s]+)")


def parse_github_repo(repo_url: str | None) -> tuple[str, str] | None:
    if not repo_url:
        return None
    m = GH_REPO_RE.search(repo_url)
    if not m:
        return None
    return m.group(1), m.group(2)


def github_repo_info(owner: str, repo: str) -> dict | None:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        return http_json(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    except Exception:
        return None


# ---- date helpers ----

def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        s = iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return None


# ---- secret detection ----

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9]{20,}", "openai_api_key"),
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "anthropic_api_key"),
    (r"AKIA[0-9A-Z]{16}", "aws_access_key"),
    (r"ghp_[A-Za-z0-9]{36,}", "github_pat"),
    (r"github_pat_[A-Za-z0-9_]{82,}", "github_fine_pat"),
    (r"npm_[A-Za-z0-9]{36}", "npm_token"),
    (r"AIza[0-9A-Za-z_-]{35}", "google_api_key"),
]


def detect_hardcoded_secrets(src: str) -> list[str]:
    found = []
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, src):
            found.append(label)
    return found


def looks_like_download_in_script(script: str) -> bool:
    s = (script or "").lower()
    return any(needle in s for needle in [
        "curl ", "curl -", "wget ", "wget -", "powershell -c", "iex ",
        "node -e", "eval(", "https://", "http://",
    ])


def classify_unpinned(deps: dict | None) -> dict:
    """Returns counts of caret/tilde/star/latest."""
    out = {"caret": 0, "tilde": 0, "star": 0, "latest": 0, "pinned": 0}
    if not deps:
        return out
    for ver in deps.values():
        if not isinstance(ver, str):
            continue
        if ver == "*":
            out["star"] += 1
        elif ver == "latest":
            out["latest"] += 1
        elif ver.startswith("^"):
            out["caret"] += 1
        elif ver.startswith("~"):
            out["tilde"] += 1
        else:
            out["pinned"] += 1
    return out


# ---- main scan ----

def scan_package(pkg: str) -> ScanResult:
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    rubric = yaml.safe_load(RUBRIC_PATH.read_text())
    signals_by_id = {s["id"]: s for s in rubric["signals"]}
    result = ScanResult(
        package=pkg, version="", verdict="UNKNOWN", score=100,
        scanned_at=now_iso, rubric_version=rubric["schema_version"],
        self_disclosure=any(pkg.startswith(p) for p in SELF_DISCLOSURE_PREFIXES),
    )

    try:
        meta = fetch_npm_metadata(pkg)
    except urllib.error.HTTPError as e:
        result.error = f"npm: HTTP {e.code}"
        result.verdict = "ERROR"
        return result
    except Exception as e:
        result.error = f"npm: {e}"
        result.verdict = "ERROR"
        return result

    latest = (meta.get("dist-tags") or {}).get("latest")
    if not latest:
        result.error = "no latest version"
        result.verdict = "ERROR"
        return result

    result.version = latest
    versions = meta.get("versions") or {}
    lvd = versions.get(latest) or {}
    times = meta.get("time") or {}
    repo = lvd.get("repository") or {}
    license_field = lvd.get("license")
    maintainers = meta.get("maintainers") or []
    created_iso = times.get("created")
    last_release_iso = times.get(latest)

    result.metadata = {
        "latest_version": latest,
        "last_release_at": last_release_iso,
        "days_since_release": days_since(last_release_iso),
        "maintainer_count": len(maintainers),
        "repository_url": repo.get("url"),
        "license": license_field,
        "created_at": created_iso,
        "days_since_created": days_since(created_iso),
    }

    triggered: list[TriggeredSignal] = []

    def fire(sig_id: str, evidence: str):
        s = signals_by_id.get(sig_id)
        if not s:
            return
        triggered.append(TriggeredSignal(
            signal_id=sig_id, deduct=s["deduct"],
            hard_block=bool(s.get("hard_block")), evidence=evidence,
            rationale=s.get("rationale", ""),
        ))

    # C4 typosquat (cheap)
    is_typo, typo_reason = detect_typosquat(pkg)
    if is_typo:
        fire("C4_name_typosquats_official", typo_reason)

    # B signals
    dsr = result.metadata["days_since_release"]
    if dsr is not None:
        if dsr > 365:
            fire("B1_last_release_over_365d", f"{dsr} days since last release")
        elif dsr > 180:
            fire("B1b_last_release_180_to_365d", f"{dsr} days since last release")
    if len(maintainers) == 1 and not result.self_disclosure:
        fire("B2_single_maintainer", "single maintainer (bus factor 1)")
    dsc = result.metadata["days_since_created"]
    if dsc is not None and dsc < 60 and not result.self_disclosure:
        fire("B3_repo_under_60d_old", f"package created {dsc} days ago")

    # A repo / license
    if not result.metadata["repository_url"]:
        fire("A5_repo_url_missing_or_mismatched", "no repository URL in package.json")
    if not license_field or license_field in ("UNLICENSED", "SEE LICENSE IN README"):
        fire("A6_no_license", f"license={license_field!r}")

    # tarball inspect
    tarball_url = (lvd.get("dist") or {}).get("tarball")
    inspect = None
    if tarball_url:
        try:
            inspect = fetch_tarball_inspect(tarball_url)
        except Exception as e:
            result.metadata["tarball_inspect_error"] = str(e)

    if inspect:
        pj = inspect.get("package_json") or {}
        scripts = inspect.get("scripts") or {}
        deps = pj.get("dependencies") or {}
        unpinned = classify_unpinned(deps)
        result.metadata["dep_count"] = sum(unpinned.values())
        result.metadata["unpinned_classification"] = unpinned

        # A1 calibrated — only fire if caret+tilde is >70% of deps AND >5 deps total
        total = sum(unpinned.values())
        if total > 5 and (unpinned["caret"] + unpinned["tilde"]) / total > 0.7:
            fire("A1_unpinned_deps", f"{unpinned['caret']} caret + {unpinned['tilde']} tilde / {total} deps (>70%)")
        # A1b — star/latest is the hard problem
        if unpinned["star"] + unpinned["latest"] > 0:
            fire("A1b_dangerous_unpinned", f"star={unpinned['star']} latest={unpinned['latest']}")

        if "postinstall" in scripts:
            fire("A2_postinstall_script", f"postinstall: {scripts['postinstall'][:120]}")
        for hook in ("preinstall", "prepack", "prepublish", "prepublishOnly"):
            if hook in scripts and looks_like_download_in_script(scripts[hook]):
                fire("A3_preinstall_or_prepack_with_download", f"{hook}: {scripts[hook][:120]}")
                break
        secrets = detect_hardcoded_secrets(inspect.get("src_concat") or "")
        if secrets:
            fire("D3_hardcoded_credentials_in_source", f"detected: {', '.join(secrets)}")

    # C1/C2/C3 — OSV API lookup (Day 2 NEW)
    osv_vulns = osv_vulns_for_package(pkg, latest)
    result.metadata["osv_vuln_count"] = len(osv_vulns)
    if osv_vulns:
        result.metadata["osv_vuln_ids"] = [v.get("id") for v in osv_vulns[:10]]
        # Classify each
        crit = high = med = 0
        for v in osv_vulns:
            sev = osv_severity(v)
            if sev == "CRITICAL":
                crit += 1
            elif sev == "HIGH":
                high += 1
            else:
                med += 1
        if crit > 0:
            fire("C1_critical_cve_in_direct_deps", f"OSV CRITICAL: {crit} (sample IDs: {', '.join([v.get('id') for v in osv_vulns[:3]])})")
        if high > 0:
            fire("C2_high_cve_in_direct_deps", f"OSV HIGH: {high}")
        if med > 0:
            fire("C3_high_or_critical_in_transitive", f"OSV MED: {med}")

    # B4 GitHub last-push staleness (Day 2 NEW)
    gh = parse_github_repo(repo.get("url"))
    if gh:
        gh_info = github_repo_info(*gh)
        if gh_info:
            last_pushed = gh_info.get("pushed_at")
            dsp = days_since(last_pushed)
            if dsp is not None:
                result.metadata["github_days_since_push"] = dsp
                if dsp > 365:
                    fire("B4_github_last_push_over_365d", f"GitHub last push {dsp} days ago ({last_pushed})")
            stars = gh_info.get("stargazers_count")
            result.metadata["github_stars"] = stars
            archived = gh_info.get("archived")
            if archived:
                fire("B5_repo_archived", "GitHub repo is archived")

    # A4 provenance attestation (rough)
    sigs = (lvd.get("dist") or {}).get("signatures") or []
    if not sigs:
        fire("A4_no_provenance_attestation", "no provenance signature in dist")

    # ---- aggregate ----
    score = 100
    hard_block_hit = False
    for t in triggered:
        score -= t.deduct
        if t.hard_block:
            hard_block_hit = True
    score = max(0, score)
    result.score = score
    result.triggered_signals = triggered

    if hard_block_hit:
        result.verdict = "BLOCK"
    elif score >= rubric["verdict_thresholds"]["pass_min"]:
        result.verdict = "PASS"
    elif score >= rubric["verdict_thresholds"]["warn_min"]:
        result.verdict = "WARN"
    else:
        result.verdict = "BLOCK"

    return result


def render_human(r: ScanResult) -> str:
    emoji = {"PASS": "✓", "WARN": "!", "BLOCK": "✗", "ERROR": "?", "UNKNOWN": "?"}.get(r.verdict, "?")
    self_tag = " [self-disclosed]" if r.self_disclosure else ""
    lines = [f"{emoji} {r.verdict}: {r.package}@{r.version}  (score {r.score}/100){self_tag}"]
    if r.error:
        lines.append(f"  ERROR: {r.error}")
        return "\n".join(lines)
    if r.triggered_signals:
        for t in r.triggered_signals:
            marker = " HARD" if t.hard_block else ""
            lines.append(f"    -{t.deduct}{marker} {t.signal_id}: {t.evidence}")
    else:
        lines.append("  clean")
    m = r.metadata
    lines.append(
        f"  m={m.get('maintainer_count')} dsr={m.get('days_since_release')} "
        f"gh_dsp={m.get('github_days_since_push')} stars={m.get('github_stars')} "
        f"deps={m.get('dep_count')} osv={m.get('osv_vuln_count')} lic={m.get('license')}"
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(prog="mcp-doctor")
    ap.add_argument("packages", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = []
    for pkg in args.packages:
        r = scan_package(pkg)
        results.append(r)
        if not args.json:
            print(render_human(r))
            print()
        time.sleep(0.4)
    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2, default=str))
    if any(r.verdict == "BLOCK" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
