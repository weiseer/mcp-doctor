---
layout: default
title: "How to audit every MCP server in your AI agent stack"
description: "How to audit every MCP server in your AI agent stack — free, zero-auth, install-time MCP supply-chain trust gate."
---

# How to audit every MCP server in your AI agent stack

Every AI agent you deploy pulls in multiple MCP servers, each a potential supply-chain risk that demands systematic auditing before production use.

Modern AI agents routinely integrate a dozen or more MCP servers for file access, database queries, API orchestration, and web browsing. Each server is a package with its own dependency tree, maintainer history, and security posture. Manually reviewing each one is impractical; you need a repeatable, bulk-vettable audit workflow.

## Why MCP servers need supply-chain auditing

MCP servers run with the same privileges as your agent process. A compromised server can exfiltrate data, inject malicious tool outputs, or pivot to internal services. The attack surface mirrors traditional npm/pip supply-chain risks but with an AI-specific twist: the server controls what the agent sees and does. Auditing must cover:

- **Maintainer trust** – single-person projects vs. teams with history
- **Release freshness** – stale packages often harbor unpatched issues
- **Dependency count** – each dependency multiplies risk
- **Known vulnerabilities** – OSV database matches
- **License compliance** – GPL/AGPL can create legal exposure
- **Hardcoded secrets** – API keys or tokens in source
- **Typosquatting risk** – packages named to mimic popular ones

## Bulk-scanning your entire MCP server stack

The `mcp-doctor` tool provides a single command that returns a verdict (`PASS`, `WARN`, or `BLOCK`) with a score out of 100, derived from all the signals above. For a one-off audit of a single server:

```bash
npx @weiseer/mcp-doctor <package>
```

For Python environments (pip-installed MCP servers):

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

But the real power for stack-wide auditing is the API endpoint, which requires zero authentication and returns structured JSON for programmatic processing.

## Bulk-audit workflow with the API

When you have 20+ MCP servers to vet, loop over them with the API:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

Example response structure (simplified):

```json
{
  "package": "@modelcontextprotocol/server-filesystem",
  "score": 85,
  "verdict": "PASS",
  "signals": {
    "maintainer_count": 3,
    "days_since_release": 14,
    "github_push_recency": "3 days ago",
    "dep_count": 12,
    "osv_vuln_count": 0,
    "license": "MIT",
    "hardcoded_secret": false,
    "typosquat_distance": 0.92
  }
}
```

A `BLOCK` verdict (score < 50) means immediate remediation. `WARN` (50–70) requires manual review. `PASS` (>70) is safe for staging but not necessarily production.

## Automating the audit pipeline

For CI/CD or scheduled audits, pipe the API results into a decision matrix:

```bash
#!/bin/bash
packages=("@modelcontextprotocol/server-filesystem" "@modelcontextprotocol/server-postgres" "mcp-server-sqlite")
for pkg in "${packages[@]}"; do
  result=$(curl -s "https://api.weiseer.com/scan?pkg=$pkg")
  verdict=$(echo "$result" | jq -r '.verdict')
  score=$(echo "$result" | jq -r '.score')
  echo "$pkg: $verdict ($score/100)"
done
```

This script can gate deployments: if any server returns `BLOCK`, fail the build and alert the team.

## When to escalate: human deep-audit for production sign-off

Automated scanning catches low-hanging fruit but cannot reason about business logic, data flow, or subtle backdoors. For production-critical MCP servers—especially those handling PII, financial data, or infrastructure access—a human deep-audit is essential.

The deep-audit service provides manual code review, dependency tree analysis, and a signed attestation for compliance. Use it when:

- The server score is `WARN` and you need production sign-off
- The server accesses sensitive data stores
- The server has fewer than 2 maintainers and >6 months since last release
- Your compliance framework (SOC 2, ISO 27001) requires human review

## Practical audit checklist for your agent stack

1. **Inventory all MCP servers** – list every `@modelcontextprotocol/*` or custom server your agent loads
2. **Bulk-scan with the API** – run the curl command for each, collect scores
3. **Triage BLOCK servers** – remove or replace immediately
4. **Review WARN servers** – check maintainer history, dependency count, and license
5. **Schedule deep-audits** – for production-bound servers, engage human review
6. **Monitor continuously** – packages can be compromised after initial audit; re-scan weekly

## Why zero-auth matters for security teams

The API requires no API key, no registration, no billing info. This eliminates friction for security engineers who want to run ad-hoc scans without provisioning credentials. It also means you can embed scanning in ephemeral CI runners without secret management.

## The bottom line

MCP servers are the new npm/pip supply-chain frontier. Bulk-audit every server in your agent stack with the `mcp-doctor` API, triage by verdict, and escalate to human deep-audit for production sign-off. Your agent is only as trustworthy as its least-vetted dependency.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_