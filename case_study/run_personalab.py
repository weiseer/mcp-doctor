#!/usr/bin/env python3
"""
personalab × mcp-doctor case study runner.

Loads 12 personas from /tmp/personalab/personas/, simulates each one's 5-day
agentic evaluation of mcp-doctor (install → first scan → leaderboard → CI
integration → pricing decision), outputs report matching PostHog case format.

Apache-2.0. Case study #4 in the personalab series.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

PERSONAS_DIR = pathlib.Path("/tmp/personalab/personas")
OUTPUT_DIR = pathlib.Path("/opt/organism/products/mcp_doctor/case_study/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-haiku-4-5-20251001"

PRODUCT_BRIEF = """
**mcp-doctor — Install-time supply-chain trust gate for MCP server packages**

GitHub: github.com/weiseer/mcp-doctor  · Live API: api.weiseer.com  · Pricing: weiseer.gumroad.com/l/hxmty

What it is: an open-source supply-chain scanner for MCP (Model Context Protocol)
server packages. CLI + GitHub Action + Trust Badge + free public API. Returns
PASS / WARN / BLOCK with cited evidence per signal. Open-source scoring rubric.

Why it exists: 2026 has seen MCPwn (CVE-2026-33032, CVSS 9.8 — 2,600+ exposed
instances), the Shai-Hulud worm that stole MCP auth tokens from 172 npm
packages, MCPSafe finding HIGH-severity bugs in *official* Atlassian/GitHub/
Cloudflare/Microsoft MCPs. Bumblebee from Perplexity launched 2026-05-22.
Real ecosystem gap.

What the 200-package validation found:
- 138 PASS (69%) / 58 WARN (29%) / 3 BLOCK (1.5%)
- 1 package had a hardcoded `sk-ant-...` Anthropic API key in published source
  (responsible disclosure in progress, name withheld until 2026-06-06)
- 2 typosquats of official @modelcontextprotocol servers
- 6 of 10 "official" @modelcontextprotocol/server-* packages stale >365 days
  with no `repository` URL in package.json
- @google/generative-ai archived by Google but still widely installed

Pricing:
- Free: single scan, Trust Badge, public leaderboard, 60 req/min/IP, no auth
- Pro $19/mo: repo monitoring, drift alerts, badge history, unlimited CI calls
- Team $49/mo: 5 repos monitored, Slack/Webhook alerts, custom policy YAML
- Enterprise $299/mo: unlimited repos, private allow/denylist, audit log export

Shipped in 14h. Built by wei@weiseer.com (solo founder, China-based, no entity).
Author: same person who built personalab.

Competitive context:
- Bumblebee (Perplexity, free open-source) — supply-chain scanner, broader, MCP-tangential
- Snyk Open Source ($98/mo/dev) — general npm CVE, no MCP-specific signals, no MCP-rubric
- MCPSafe — research-grade scans, not a productized tool
- npm audit (free, built-in) — CVE-only, no maintainer health, no typosquat
- No direct "MCP supply chain trust gate" competitor yet

Open-source rubric is at github.com/weiseer/mcp-doctor/blob/main/rubric.yaml — 20+
signals across 4 categories (supply chain hygiene, maintainer health, vulnerability,
MCP-specific). Calibrated against 200 real packages.

Trust badge:  ![MCP Trust](https://api.weiseer.com/badge?pkg=YOUR_PACKAGE)
""".strip()

EVENTS = [
    {
        "day": 1,
        "title": "Discovery via Twitter/HN/Reddit",
        "body": "You see a post: 'I scanned 200 popular MCP server packages — 1 had hardcoded LLM API key, 6 official packages stale >365 days. Open-source rubric.' Link to github.com/weiseer/mcp-doctor. You click through, skim the README, look at the leaderboard."
    },
    {
        "day": 2,
        "title": "First scan — your own packages",
        "body": "You run `npx @weiseer/mcp-doctor @some/mcp-server-you-use`. Get a WARN verdict (score 67) with 3 triggered signals: 416 days since last release, no repository URL, 6 caret deps. The output is detailed; cites a source URL per signal. You're not sure if WARN means 'do not install' or 'be aware'."
    },
    {
        "day": 3,
        "title": "GitHub Action suggestion in DM/Slack",
        "body": "A colleague pings you: 'should we add weiseer/mcp-doctor-action@v1 to our CI?' They link the action.yml. Policy options: strict / block-only / report. You think about whether you want PRs blocked when WARN packages enter the dependency tree, or just blocked on BLOCK."
    },
    {
        "day": 4,
        "title": "Pricing question — Pro tier landing",
        "body": "You visit weiseer.gumroad.com/l/hxmty. Pro is $19/mo: 'repo monitoring + drift alerts + badge history + unlimited CI'. You ask yourself: am I getting enough value from the free tier (60 req/min/IP, public scan + badge)? Or do I need Pro for the alerting?"
    },
    {
        "day": 5,
        "title": "Decision day — keep using? subscribe? abandon?",
        "body": "You've used mcp-doctor 4 days. The free tier scan + badge is genuinely useful. You found a stale package in your stack. You also noticed the rubric flagged @modelcontextprotocol/server-github as WARN, which felt weird (it's 'official'). You're deciding: do I subscribe to Pro? Stay free? Uninstall and switch to npm audit + manual review?"
    },
]


def call_claude(system: str, user: str) -> str:
    payload = {
        "model": MODEL,
        "max_tokens": 800,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "temperature": 0.4,
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.load(r)
        return d["content"][0]["text"] if d.get("content") else ""


SYSTEM_PROMPT = """你扮演一个被给定的人格，正在评估一款叫 mcp-doctor 的产品。

每次我会告诉你今天是第几天，你今天看到了什么。

你的任务:
1. 严格按人格反应(不要变成"理性 AI"——人格是什么样,反应就是什么样)
2. 给出一个动作:DO_NOTHING / SUBSCRIBE_PRO / SUBSCRIBE_TEAM / SUBSCRIBE_ENTERPRISE / UNSUBSCRIBE_OR_UNINSTALL / SHARE_WITH_TEAM / OPEN_GITHUB_ISSUE
3. 简短理由(1-2 句话,人格腔调)
4. 心情:curious / engaged / annoyed / considering_quit / decided

返回 JSON 格式:
{
  "action": "...",
  "mood": "...",
  "engage_score": 1-10,
  "reason": "...",
  "verbatim_quote": "如果你今天会在 Twitter 上发一条关于 mcp-doctor 的推,会写什么(可空)"
}"""


def run_persona(persona_path: pathlib.Path) -> dict:
    persona_body = persona_path.read_text()
    persona_id = persona_path.stem
    print(f"\n=== {persona_id} ===", file=sys.stderr)

    history = []
    days = []
    for event in EVENTS:
        history_str = "\n".join(
            f"- Day {h['day']}: {h['action']} — {h['reason'][:80]}"
            for h in history
        ) or "(none yet)"

        user_msg = f"""# 你的人格
{persona_body}

---

# 产品背景(你需要知道的)
{PRODUCT_BRIEF}

---

# 今天: 第 {event['day']} 天 / 共 5 天
**触发事件**: {event['title']}

{event['body']}

# 你前几天的动作
{history_str}

请只返回 JSON,不要其他东西。
"""
        try:
            response = call_claude(SYSTEM_PROMPT, user_msg)
            # Parse JSON
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(response[start:end])
            else:
                data = {"action": "PARSE_ERROR", "mood": "error", "reason": response[:120]}
        except Exception as e:
            data = {"action": "ERROR", "mood": "error", "reason": str(e)[:120]}

        data["day"] = event["day"]
        days.append(data)
        history.append({"day": event["day"], "action": data.get("action"), "reason": data.get("reason", "")})

        print(f"  day {event['day']}: {data.get('action')} ({data.get('mood', '?')})", file=sys.stderr)
        time.sleep(0.3)

    return {"persona": persona_id, "days": days}


def aggregate(results: list[dict]) -> dict:
    summary = []
    for r in results:
        # Final action
        actions = [d.get("action") for d in r["days"]]
        last = actions[-1] if actions else "?"
        will_pay = any(a in ("SUBSCRIBE_PRO", "SUBSCRIBE_TEAM", "SUBSCRIBE_ENTERPRISE") for a in actions)
        unsubscribed = any(a == "UNSUBSCRIBE_OR_UNINSTALL" for a in actions)
        summary.append({
            "persona": r["persona"],
            "final_action": last,
            "will_pay": will_pay,
            "unsubscribed": unsubscribed,
            "actions": actions,
            "verbatim": next((d.get("verbatim_quote") for d in r["days"] if d.get("verbatim_quote")), None),
        })
    return {
        "case": "mcp-doctor",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "persona_count": len(results),
        "would_pay_count": sum(1 for s in summary if s["will_pay"]),
        "unsubscribed_count": sum(1 for s in summary if s["unsubscribed"]),
        "results": results,
        "summary": summary,
    }


def main():
    if not PERSONAS_DIR.exists():
        print(f"  ERROR: personas dir missing at {PERSONAS_DIR}", file=sys.stderr)
        return 2

    persona_paths = sorted(PERSONAS_DIR.glob("*.md"))
    print(f"  running case study with {len(persona_paths)} personas × 5 days", file=sys.stderr)
    results = []
    for p in persona_paths:
        results.append(run_persona(p))

    final = aggregate(results)
    out_path = OUTPUT_DIR / "mcp_doctor_personalab_report.json"
    out_path.write_text(json.dumps(final, ensure_ascii=False, indent=2))
    print(f"\n  raw report -> {out_path}", file=sys.stderr)
    print(f"\n  would pay: {final['would_pay_count']}/{final['persona_count']}", file=sys.stderr)
    print(f"  unsubscribed: {final['unsubscribed_count']}/{final['persona_count']}", file=sys.stderr)


if __name__ == "__main__":
    main()
