---
layout: default
title: "How to detect a typosquatted MCP server on npm"
description: "How to detect a typosquatted MCP server on npm — free, zero-auth, install-time MCP supply-chain trust gate."
---

# How to detect a typosquatted MCP server on npm

Typosquatting is one of the oldest supply-chain attacks, and the MCP ecosystem is a prime target: attackers publish packages with names like `@modelcontextprotocol/server-filesystem` (note the swapped vowel) or `modelcontextprotocol-server-filesystem` (missing the `@` scope) to trick developers into installing malicious code instead of the official `@modelcontextprotocol/server-filesystem`. A single character change can route your build to a package that exfiltrates secrets or backdoors your agent. Here is how to detect these fake MCP servers on npm using a free, zero-auth scan that flags them with a BLOCK verdict.

## How typosquatting works against MCP packages

The official MCP servers live under the `@modelcontextprotocol` npm scope—for example, `@modelcontextprotocol/server-filesystem`, `@modelcontextprotocol/server-github`, and `@modelcontextprotocol/server-slack`. Attackers exploit three patterns:

- **Character swaps** – `@modelcontextprotocl/server-filesystem` (transposed "ol" → "lo")
- **Missing scope** – `modelcontextprotocol-server-filesystem` (no `@`, looks like a different package)
- **Homoglyphs** – replacing an "o" with a Cyrillic "о" that renders identically in most terminals

These packages often contain a small wrapper that calls home with your MCP credentials or environment variables before proxying to the real server. Because `npm install` does not verify the publisher identity, a developer typing `npm install @modelcontextprotocol/server-filesystem` with a typo gets the fake.

## Why edit-distance detection catches them

Edit distance (Levenshtein distance) measures how many single-character changes are needed to turn one string into another. A typosquatted MCP server typically has an edit distance of 1–3 from the legitimate name. The `mcp-doctor` scanner computes this distance against a known-safe registry of official MCP packages. When the distance is small (≤3) **and** the package is not the official one, the scanner raises a BLOCK.

The scanner also cross-references the package name against a database of known typosquatting patterns (e.g., missing `@`, common transpositions). This catches not just exact edit-distance matches but also structural lookalikes.

## Running the free scan

You do not need an account or API key. For any npm package, run:

```bash
npx @weiseer/mcp-doctor <package>
```

Replace `<package>` with the suspicious name. For example, if you suspect `@modelcontextprotocl/server-filesystem`:

```bash
npx @weiseer/mcp-doctor @modelcontextprotocl/server-filesystem
```

The tool outputs a verdict of **PASS**, **WARN**, or **BLOCK** with a score out of 100. A BLOCK means the scanner has high confidence this is a typosquat or malicious package. The score is derived from multiple signals:

- **Maintainer count** – official packages have 3+ maintainers; typosquats often have 1
- **Days since release** – fake packages are usually very new
- **GitHub push recency** – no recent commits to a linked repo
- **Dependency count** – suspiciously few or many compared to the official version
- **OSV vulnerability count** – known CVEs in the package or its deps
- **License** – missing or non-standard license
- **Hardcoded secret detection** – API keys or tokens in the source
- **Typosquat distance** – the edit-distance check against official names

If the package is a clear typosquat, you will see something like:

```
BLOCK (score: 12/100) — Typosquat distance 1 from @modelcontextprotocol/server-filesystem
```

## Scanning via API for CI/CD pipelines

For automated checks in pre-commit hooks or CI, use the API directly:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

This returns JSON with the same verdict and score. You can parse the `verdict` field and fail the build on BLOCK. No authentication required.

## What to do when you find a typosquat

1. **Do not install it** – if you already did, revoke any tokens or keys the package may have accessed.
2. **Report to npm** – use `npm owner ls <package>` to find the publisher, then report via `npm report`.
3. **Notify your team** – add the package name to a blocklist in your `.npmrc` or internal registry.
4. **Scan your lockfile** – run `mcp-doctor` on every dependency in `package-lock.json` to catch any already-installed typosquats.

## Prevention in your workflow

- Always copy-paste the exact `@modelcontextprotocol/server-*` name from the official docs—never type it manually.
- Add a pre-install hook that runs `mcp-doctor` on any new dependency before `npm install` completes.
- Pin versions: `@modelcontextprotocol/server-filesystem@0.1.0` instead of `^0.1.0` to avoid accidental typosquat upgrades.

The MCP ecosystem is growing fast, and attackers are watching. A single character is all it takes to turn a trusted server into a backdoor. Run the free scan before every install.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_