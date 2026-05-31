---
layout: default
title: "How to gate MCP servers in CI with a free GitHub Action"
description: "How to gate MCP servers in CI with a free GitHub Action — free, zero-auth, install-time MCP supply-chain trust gate."
---

# How to gate MCP servers in CI with a free GitHub Action

Block unsafe MCP servers before they ever reach production by adding a deterministic, evidence-backed gate directly into your CI pipeline. The `weiseer/mcp-doctor-action` GitHub Action runs `mcp-doctor` against every MCP server dependency in your project and fails the build on any package that receives a `BLOCK` verdict, giving you a cited, auditable reason for the rejection.

## Why MCP servers need a CI gate

MCP servers run as local subprocesses with full filesystem and network access. Unlike traditional npm or PyPI packages, a malicious MCP server can exfiltrate environment variables, read SSH keys, or modify source code in real time. Standard vulnerability scanners (Snyk, Dependabot) only check for known CVEs—they miss typosquatted packages, zero-day malware, hardcoded secrets, and supply-chain indicators like abandoned maintenance or suspicious license changes.

`mcp-doctor` fills this gap by scoring each package on nine deterministic signals: maintainer count, days since last release, GitHub push recency, dependency count, OSV vulnerability count, license type, presence of hardcoded secrets, and typosquat distance from popular packages. The verdict is `PASS` (safe), `WARN` (proceed with caution), or `BLOCK` (do not use). Every `BLOCK` verdict includes the specific signals that triggered it, so you can audit the decision.

## Setting up the GitHub Action

Add a workflow file at `.github/workflows/mcp-doctor.yml`:

```yaml
name: MCP Server Security Gate
on: [pull_request]

jobs:
  scan-mcp-servers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: weiseer/mcp-doctor-action@v1
        with:
          package-manager: npm   # or 'pip'
          fail-on: BLOCK
```

This action automatically detects your `package.json` or `requirements.txt`, runs `mcp-doctor` on every MCP server listed, and exits with code 1 if any package scores `BLOCK`. The `fail-on: BLOCK` parameter is the strictest gate—it allows `WARN` packages through but stops `BLOCK` ones.

For a more conservative policy, set `fail-on: WARN` to also block packages with suspicious but not definitive signals.

## What happens when a package is blocked

When a pull request introduces a blocked MCP server, the action outputs a detailed report in the workflow logs:

```
❌ BLOCK: @malicious/mcp-server (score: 12/100)
   - typosquat distance: 0.92 from @anthropic/mcp-server
   - maintainer count: 1 (solo account, 3 days old)
   - days since release: 0
   - hardcoded-secret: found AWS key in source
```

The PR check shows a red ❌ status, preventing merge. The developer can click "Details" to see the exact evidence. This is deterministic—rerunning the same scan on the same package always produces the same verdict, because `mcp-doctor` uses only static, verifiable signals from public registries and GitHub APIs.

## Scanning without the action

You can also run `mcp-doctor` directly in any CI step or locally:

```bash
npx @weiseer/mcp-doctor <package>
```

For Python projects:

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

Or via the API for scripting:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

All three methods return the same verdict and score, so you can integrate into any CI system (GitLab CI, Jenkins, CircleCI) by parsing the JSON output.

## Interpreting the score

The score is 0–100, derived from weighted signals:

- **Maintainer count** (0–20): Fewer than 2 maintainers drops the score significantly.
- **Days since release** (0–15): A package released today with no history scores low.
- **GitHub push recency** (0–15): No commits in 6+ months indicates abandonment.
- **Dependency count** (0–10): Zero dependencies is suspicious for a server.
- **OSV vulnerabilities** (0–10): Any known CVE reduces score.
- **License** (0–10): Missing or proprietary license flags.
- **Hardcoded secrets** (0–10): API keys or tokens in source.
- **Typosquat distance** (0–10): Distance < 0.95 from a popular package triggers warning.

A score below 40 typically results in `BLOCK`, but the verdict is based on the combination of signals, not a simple threshold.

## Why not just use npm audit or pip-audit?

Traditional audit tools check for known vulnerabilities in the dependency tree. They do not detect:

- Typosquatted packages (e.g., `@anthropic-mcp-server` vs `@anthropic/mcp-server`)
- Packages with hardcoded secrets
- Abandoned packages with no recent maintenance
- Packages with suspicious license changes
- Single-maintainer packages with no history

`mcp-doctor` catches these because it evaluates the package itself, not just its known CVEs. For MCP servers—which execute arbitrary code with high privileges—this breadth of signals is critical.

## Best practices for your CI gate

1. **Run on every PR**, not just on merge to main. Blocking early saves debugging time.
2. **Use `fail-on: BLOCK`** initially, then tighten to `WARN` after your team reviews the false-positive rate.
3. **Pin the action version** (`@v1` is a moving tag; use `@v1.0.0` for production).
4. **Review blocked packages manually** before overriding—the cited evidence makes this fast.
5. **Combine with Dependabot** for CVE coverage and `mcp-doctor` for supply-chain signals.

## Example: blocking a typosquatted package

A developer accidentally adds `@anthropic-mcp-server` (typosquatting `@anthropic/mcp-server`). The action runs:

```
❌ BLOCK: @anthropic-mcp-server (score: 8/100)
   - typosquat distance: 0.88 from @anthropic/mcp-server
   - maintainer count: 1
   - days since release: 0
   - hardcoded-secret: found in source
```

The PR is blocked. The developer removes the package, adds the correct one, and the next run passes.

## Conclusion

Gating MCP servers in CI with `mcp-doctor` is a deterministic, auditable, and free way to prevent supply-chain attacks before they reach your codebase. The GitHub Action integrates in minutes, requires no authentication, and provides cited evidence for every blocked package. For continuous monitoring of approved packages, consider the Pro tier; for production sign-off, the human deep-audit service adds an extra layer of assurance.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_