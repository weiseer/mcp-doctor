---
layout: default
title: "An install-time trust gate for MCP servers: PASS / WARN / BLOCK explained"
description: "An install-time trust gate for MCP servers: PASS / WARN / BLOCK explained — free, zero-auth, install-time MCP supply-chain trust gate."
---

# An install-time trust gate for MCP servers: PASS / WARN / BLOCK explained

An install-time trust gate for MCP servers: PASS / WARN / BLOCK explained

When you run `npx @weiseer/mcp-doctor <package>` or hit the API, you get back a deterministic verdict—PASS, WARN, or BLOCK—alongside a score out of 100. This isn’t a black-box reputation score; it’s a transparent composite of eight cited signals, each independently verifiable. The gate is designed to be reproducible and defensible: two engineers scanning the same package at the same moment get the same verdict. Here’s how each signal contributes, and why this matters for MCP server installation decisions.

## The verdict system

The three-tier output is simple: **PASS** means the package clears all risk thresholds and is safe to install. **WARN** flags moderate concerns—you should review the cited signals before trusting it. **BLOCK** means one or more critical signals (e.g., a known OSV vulnerability, a hardcoded secret, or a typosquat distance under a threshold) triggered an automatic denial. The score/100 is a weighted sum of the eight signals, normalized so that a perfect package scores 100 and a blocked package typically scores below 40.

## The eight cited signals

Every scan report lists these signals with their raw values and contribution to the score:

1. **Maintainer count** – Number of distinct maintainers on the package. Fewer than 2 maintainers for a production MCP server is a WARN signal; a single maintainer with no history is a BLOCK.
2. **Days since last release** – Freshness. A release older than 365 days triggers a WARN; older than 730 days is a BLOCK.
3. **GitHub push recency** – Last commit on the default branch. Stale repos (no pushes in 180 days) get a WARN; abandoned repos (no pushes in 365 days) get a BLOCK.
4. **Dependency count** – Number of runtime dependencies. High dependency trees (above 50) increase attack surface and lower the score, but don’t directly cause a BLOCK unless combined with other signals.
5. **OSV vulnerability count** – Known vulnerabilities from the Open Source Vulnerabilities database. Any unpatched OSV entry with a severity of HIGH or CRITICAL triggers an automatic BLOCK.
6. **License** – Missing or non-standard license (not in the SPDX approved list) is a WARN. A clearly proprietary or non-OSI-approved license is a BLOCK.
7. **Hardcoded secret** – Scanned for API keys, tokens, or credentials in the package source. Any hardcoded secret is an automatic BLOCK.
8. **Typosquat distance** – Levenshtein distance to the top 1,000 most-downloaded npm packages. A distance of 1 or 2 (e.g., `express` vs `exprees`) is a BLOCK; distance 3 is a WARN.

## Reproducible and defensible

Because every signal is a measurable fact—not a heuristic or ML model—you can audit the verdict. If the API returns BLOCK due to an OSV vulnerability, you can look up that CVE yourself. If it flags a typosquat, you can compute the Levenshtein distance manually. This makes the gate suitable for CI/CD pipelines where you need an auditable security decision.

## Using the scan

To scan an npm package, run:

```bash
npx @weiseer/mcp-doctor <package>
```

For pip-installable Python packages, first install the tool, then run:

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

Both commands output a JSON report with the verdict, score, and all eight signal values. The CLI is zero-auth—no API key needed.

## Using the API directly

For automation, hit the API with a simple GET request:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

The response is a JSON object with `verdict`, `score`, and `signals`. The API is also free and zero-auth, so you can integrate it into pre-install hooks, package.json scripts, or your own tooling without registration.

## When to use each verdict

- **PASS** – Install without additional review. The package is actively maintained, has multiple maintainers, no known vulnerabilities, no secrets, and isn’t a typosquat.
- **WARN** – Investigate the flagged signals. For example, a single maintainer with a recent release and no vulnerabilities might be acceptable for a small MCP server, but you should verify the maintainer’s reputation.
- **BLOCK** – Do not install. The package has a critical vulnerability, a hardcoded secret, or is likely a typosquat. Investigate the specific signal before considering any override.

## Why this matters for MCP servers

MCP servers run locally and often have filesystem or network access. A compromised MCP server can exfiltrate data, modify files, or execute arbitrary commands. The install-time trust gate gives you a deterministic, repeatable check before you run `npx` or `pip install` on an untrusted package. It doesn’t replace a full security audit, but it catches the most common attack vectors—typosquatting, abandoned packages, known vulnerabilities, and leaked credentials—at the moment of installation.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_