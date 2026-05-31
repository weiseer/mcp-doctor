---
layout: default
title: "How to check if an npm/MCP package ships a hardcoded API key"
description: "How to check if an npm/MCP package ships a hardcoded API key — free, zero-auth, install-time MCP supply-chain trust gate."
---

# How to check if an npm/MCP package ships a hardcoded API key

A published npm or MCP package can embed a live API key (e.g., `sk-...`, `AKIA...`, `ghp_...`) that an attacker can extract from the bundle in seconds, yet most developers never check for this before installing. The free, zero-auth `@weiseer/mcp-doctor` scanner surfaces a dedicated `hardcoded-secret` signal that flags exactly this risk, scoring it alongside eight other supply-chain signals.

## Why hardcoded keys in npm packages are dangerous

When a package author commits a real API key—whether accidentally in a config file, a test fixture, or a `.env` that got bundled—that secret becomes part of the published tarball. Anyone running `npm install <package>` pulls the entire source tree, including any hardcoded credentials. Attackers scrape npm registries for patterns like `sk-` (OpenAI), `AKIA` (AWS), or `ghp_` (GitHub PAT) and can use those keys within minutes to drain quotas, access private data, or pivot into cloud infrastructure.

The problem is especially acute for MCP (Model Context Protocol) packages, which often bundle provider API keys to enable AI tool calls. A single leaked key in a popular MCP server can compromise every user who installs it.

## How the free scan detects hardcoded secrets

The `@weiseer/mcp-doctor` scanner performs a static analysis of the published package (not your local checkout) and reports a `hardcoded-secret` signal as one of nine evidence categories. It does not require authentication, API keys, or a running service—just a package name.

Run it on any npm package with:

```bash
npx @weiseer/mcp-doctor <package>
```

For Python packages (PyPI), install the CLI and run:

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

You can also call the API directly for scripting or CI:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

The scanner returns a verdict of **PASS**, **WARN**, or **BLOCK** with a score out of 100. The `hardcoded-secret` signal contributes to the score based on the number and severity of secrets detected. If the scanner finds a live API key pattern (e.g., a valid-format OpenAI key, AWS access key, or GitHub token), it will issue a WARN or BLOCK verdict depending on the key's apparent validity and whether it matches known provider formats.

## What the secret-scan signal checks

The scanner's secret detector looks for:

- **Provider-specific patterns**: `sk-` prefixed keys (OpenAI, Anthropic), `AKIA` (AWS IAM), `ghp_` / `gho_` (GitHub), `xoxb-` / `xoxp-` (Slack), and dozens more.
- **High-entropy strings in suspicious contexts**: Any string that looks like a random token in a config file, `.env`, or source code.
- **False-positive filtering**: Common test keys, example keys (e.g., `sk-your-key-here`), and known placeholder values are excluded to reduce noise.

The scanner does **not** attempt to validate the key against the provider's API (that would require network calls and risk rate-limiting). Instead, it uses format-based detection: if a string matches the exact format of a live provider key (correct prefix, character set, and length), it flags it.

## Interpreting the results

A typical output for a package with a hardcoded secret might show:

```
hardcoded-secret: BLOCK (3 secrets found)
  - OpenAI API key in src/config.ts:12
  - AWS access key in .env.example:4
  - GitHub token in test/fixtures/auth.json:7
```

The overall score drops significantly—often below 50/100—because a single live secret is a critical supply-chain risk. The scanner also reports other signals (maintainer count, days-since-release, GitHub push recency, dependency count, OSV vulnerability count, license, typosquat distance) so you can see the full risk profile.

## Practical workflow for CI/CD

Add the scan to your pre-install pipeline. For example, in a GitHub Actions workflow:

```yaml
- name: Scan package for secrets
  run: npx @weiseer/mcp-doctor ${{ matrix.package }}
```

If the verdict is BLOCK, fail the build. For WARN, log the finding and allow manual review. Because the scanner is zero-auth and free, there is no credential management or rate limit to worry about.

## Limitations to understand

The scanner detects **format-based** secrets, not contextual secrets. A key that uses an uncommon format (e.g., a custom base64-encoded token) may not be flagged. Conversely, a test key that happens to match a provider format (e.g., `sk-test-1234567890abcdef`) could trigger a false positive. Always verify flagged secrets manually before reporting to a package maintainer.

The scanner also cannot detect secrets that are fetched at runtime from environment variables or external services—it only analyzes the static bundle. If a package downloads a key from a remote server during install, that is a separate class of risk (dependency confusion or supply-chain attack) that the scanner's other signals may catch.

## Why this matters for MCP packages

MCP packages are particularly sensitive because they often require API keys to function as AI tool servers. A package that bundles a key "for convenience" is a ticking bomb. The scanner's `hardcoded-secret` signal gives you immediate visibility before you run `npx @modelcontextprotocol/server-whatever`.

## Next steps

Run the scan on any package you are considering for production use. The API is the fastest for automation:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

For continuous monitoring of your dependencies, the Pro tier watches for new releases and re-scans automatically. If you need a human deep-audit for production sign-off, that service is also available.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_