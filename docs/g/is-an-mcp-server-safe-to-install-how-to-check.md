---
layout: default
title: "Is an MCP server safe to install? How to check before you add it"
description: "Is an MCP server safe to install? How to check before you add it — free, zero-auth, install-time MCP supply-chain trust gate."
---

# Is an MCP server safe to install? How to check before you add it

MCP servers run with your agent's privileges, tokens, and often direct filesystem or API access, making an unvetted installation a supply-chain risk that can expose credentials or exfiltrate data the moment you run it. The fastest way to check before you add one is a single command that returns a verdict and score with cited evidence.

## Why MCP servers demand extra scrutiny

Unlike a typical npm dependency that runs in a sandboxed build step, an MCP server executes in your agent's runtime environment. It can read environment variables, access local files, make outbound network calls, and use the OAuth tokens or API keys you've configured. A malicious or compromised MCP server can steal those secrets on first run, without any visible symptoms.

The threat is not theoretical. Supply-chain attacks on package registries have become routine, and MCP servers represent a new, high-privilege attack surface. You need a repeatable way to vet them before `npx` or `pip` ever executes the package's code.

## The one-command free check

The tool `mcp-doctor` performs a static analysis of any MCP server package without installing or running it. It returns a verdict of **PASS**, **WARN**, or **BLOCK** along with a score out of 100, based on multiple signals extracted from the package metadata and public databases.

For npm packages:
```bash
npx @weiseer/mcp-doctor <package>
```

For PyPI packages:
```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

You can also use the zero-auth API directly:
```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

The output includes the verdict, score, and a breakdown of each signal that contributed to the result.

## What the score and verdict actually mean

The score out of 100 is not arbitrary. It is computed from seven categories of evidence, each weighted by severity:

- **Maintainer count** – Single-maintainer packages with no track record score lower. A team of multiple active maintainers suggests better security hygiene.
- **Days since release** – Very new packages (released days ago) have not had time for community scrutiny or vulnerability discovery. Older, stable releases score higher.
- **GitHub push recency** – A package whose repository has no recent commits may be abandoned. Abandoned packages accumulate unpatched vulnerabilities.
- **Dependency count** – Each dependency is a potential attack vector. Packages with zero or minimal dependencies reduce the blast radius.
- **OSV vulnerability count** – The tool queries the Open Source Vulnerabilities database. Any known CVEs directly lower the score.
- **License** – Missing or non-standard licenses are a red flag. Well-known open-source licenses (MIT, Apache-2.0, BSD) indicate proper governance.
- **Hardcoded secrets** – The scanner checks for embedded API keys, tokens, or credentials in the package source. This is an immediate BLOCK signal.
- **Typosquat distance** – The tool compares the package name against popular MCP servers using edit-distance algorithms. A suspiciously similar name (e.g., `@modelcontextprotocol/server-fillesystem` instead of `filesystem`) triggers a warning.

A **BLOCK** verdict means one or more critical signals (hardcoded secrets, known OSV vulnerabilities, or a confirmed typosquat) were detected. **WARN** indicates moderate risk from factors like a single maintainer, very recent release, or high dependency count. **PASS** means no red flags were found across all signals.

## Practical workflow for vetting any MCP server

Before you run `npx` or `pip install` on an MCP server package:

1. **Run the scan first** – Use the CLI or API to get the verdict and score.
2. **Review the evidence breakdown** – Look at which signals contributed to the score. A WARN due to "new package" may be acceptable if you trust the author; a WARN due to "high dependency count" warrants deeper inspection.
3. **Check the maintainer history** – If the package has a single maintainer and was released yesterday, consider waiting for community validation.
4. **Verify the package name** – Typosquatting is common. Compare the name character-by-character against the official MCP server you intended to install.

For production deployments where you need formal sign-off, a human deep-audit of the package source code is the only way to achieve full confidence. The automated scan catches the obvious risks but cannot reason about obfuscated payloads or logic bombs.

## What the scan does not do

`mcp-doctor` performs static analysis on package metadata and publicly indexed source. It does not execute the package code, so it cannot detect runtime behaviors like conditional data exfiltration (code that only activates after a certain date or on specific inputs). It also cannot verify that the published package matches the source repository (reproducible builds). These limitations are why the tool is a first-pass filter, not a final security audit.

## When to use the API vs the CLI

The API requires no installation and no authentication:
```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

This is ideal for CI/CD pipelines or quick one-off checks. The CLI (`npx @weiseer/mcp-doctor`) is more convenient for interactive use and provides formatted output. Both return the same verdict, score, and evidence.

## Bottom line

MCP servers are high-risk by design because they run with your agent's privileges. The one-command scan gives you an immediate, evidence-based verdict before you ever execute the package. Use it as your first line of defense against supply-chain attacks targeting the MCP ecosystem.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_