---
layout: default
title: "How to spot an abandoned or unmaintained MCP server"
description: "How to spot an abandoned or unmaintained MCP server — free, zero-auth, install-time MCP supply-chain trust gate."
---

# How to spot an abandoned or unmaintained MCP server

Many "official-looking" MCP server packages on npm have no recent release and no repository URL, making it impossible to verify the source behind the binary you are about to run. Here is exactly how to surface those abandonment signals before you install.

## Why unmaintained MCP servers are a security risk

MCP (Model Context Protocol) servers run with filesystem, network, and shell access. An abandoned package means no security patches, no community oversight, and often a dangling maintainer account that can be hijacked. The most dangerous signal is a missing `repository` field in `package.json` — you cannot audit the source code, so you are running a black box.

## The two critical signals: days-since-release and missing repo

The `mcp-doctor` tool surfaces exactly these two signals in its verdict. It checks:

- **Days since last release**: any package with >365 days since the last npm publish is flagged. MCP servers should release at least quarterly.
- **Repository URL presence**: if `package.json` lacks a `repository` field, the scan reports a missing-repo signal. This is a hard block for any production use.

## Scan any npm MCP package with one command

```bash
npx @weiseer/mcp-doctor <package>
```

Replace `<package>` with the exact npm package name. The tool outputs a verdict of `PASS`, `WARN`, or `BLOCK` with a score out of 100. A `BLOCK` verdict with a missing-repo signal means you should never run that server.

## Example: scanning a suspicious MCP server

```bash
npx @weiseer/mcp-doctor @example/mcp-filesystem-server
```

The output will show:
- `days-since-release: 540` (flagged)
- `has-repo-url: false` (flagged)
- `verdict: BLOCK`
- `score: 32/100`

The score is derived from eight signals: maintainer count, days-since-release, GitHub push recency, dependency count, OSV vulnerability count, license, hardcoded-secret detection, and typosquat distance. A low score with a missing repo is a definitive red flag.

## For Python packages (pip)

If the MCP server is distributed via PyPI, use the pip-installed version:

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

The same signals apply. Python packages without a `homepage` or `project_urls` pointing to a repository are equally risky.

## Zero-auth API for CI/CD pipelines

You can integrate this check into your CI without any authentication:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

Returns JSON with all signals. Parse the `verdict` field — if it is `BLOCK`, fail the build. This is free and requires no API key.

## What to do when you find an abandoned MCP server

1. **Do not install it.** Even if it works today, it will not receive security patches.
2. **Search for an active fork.** Check GitHub for forks with recent commits.
3. **Pin to the last known-good version** if you must use it temporarily, but plan a migration.
4. **Report the package** to npm via `npm owner ls <package>` to see if the maintainer is reachable.

## The missing-repo attack surface

A package without a repository URL means:
- No way to verify the build matches the source
- No issue tracker for reporting bugs
- No way to see if the maintainer is active
- Higher risk of account takeover (no linked GitHub identity)

This is why `mcp-doctor` treats missing-repo as a hard signal. Even if the package has zero vulnerabilities today, the lack of verifiability makes it a supply-chain risk.

## Automate scanning in your workflow

Add this to your `package.json` scripts or CI step:

```bash
npx @weiseer/mcp-doctor @example/mcp-server && npm install @example/mcp-server
```

If the scan returns `BLOCK`, the install never happens. For continuous monitoring of installed packages, use the Pro tier which watches for new releases and vulnerability disclosures.

## Summary

Abandoned MCP servers are a real threat because they run with elevated permissions and cannot be audited. The two fastest signals are days-since-release and missing repository URL. Use `mcp-doctor` to surface both before you install, and never trust a package that blocks on either signal.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_