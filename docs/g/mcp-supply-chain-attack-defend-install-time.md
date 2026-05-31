---
layout: default
title: "MCP supply-chain attacks (Shai-Hulud, MCPwn): defending at install time"
description: "MCP supply-chain attacks (Shai-Hulud, MCPwn): defending at install time — free, zero-auth, install-time MCP supply-chain trust gate."
---

# MCP supply-chain attacks (Shai-Hulud, MCPwn): defending at install time

Recent npm/MCP supply-chain incidents—a token-stealing worm that propagated through the MCP ecosystem and a class of vulnerabilities enabling arbitrary command execution via malicious MCP servers—have made install-time gating a non-negotiable part of any AI engineer's security posture. These attacks exploit the trust model of package registries, where a single compromised dependency can exfiltrate API keys, environment variables, or model weights before your application even initializes.

The core problem is that traditional vulnerability scanning happens after installation. By then, a malicious package's `postinstall` script has already executed. The Shai-Hulud-class worm demonstrated this by spreading through npm's dependency graph, stealing tokens from CI environments. Similarly, the MCPwn-class of CVEs (CVE-2026-33032 pattern) allowed attackers to craft MCP servers that, when installed, would execute arbitrary shell commands via the MCP protocol's tool-calling mechanism.

Install-time gating flips this model: you evaluate a package's trustworthiness *before* `npm install` or `pip install` runs. This requires a tool that can assess multiple risk signals without requiring authentication or network access to a private database.

## The install-time trust gate

The `mcp-doctor` tool provides exactly this gate. It's free, zero-auth, and works at the command line or via API. The scan verdicts are `PASS`, `WARN`, or `BLOCK`, each with a score out of 100. The score is derived from eight signals:

- **Maintainer count**: single-maintainer packages are higher risk.
- **Days since release**: very new packages lack community vetting.
- **GitHub push recency**: abandoned repos are red flags.
- **Dependency count**: more deps = larger attack surface.
- **OSV vulnerability count**: known CVEs in the package or its transitive deps.
- **License**: missing or non-standard licenses are suspicious.
- **Hardcoded secrets**: credentials baked into the package.
- **Typosquat distance**: how close the name is to a popular package.

## Scanning an npm package before install

To gate an npm package at install time, run:

```bash
npx @weiseer/mcp-doctor <package>
```

This will output a verdict. If it returns `BLOCK` (score < 50), do not install. `WARN` (score 50–79) means proceed with caution. `PASS` (score 80+) is safe to install.

For example, scanning a package named `mcp-server-filesystem`:

```bash
npx @weiseer/mcp-doctor mcp-server-filesystem
```

The tool fetches metadata from npm, GitHub, and OSV, then computes the score. No API key needed.

## Scanning a Python package before pip install

For Python packages used in MCP servers or AI pipelines:

```bash
pip install weiseer-mcp-doctor
mcp-doctor <package>
```

This works identically to the npm version, querying PyPI and the same signal sources. Use it before `pip install` in your Dockerfiles or CI scripts.

## API-based gating for automation

For CI/CD pipelines or automated install scripts, use the API directly:

```bash
curl "https://api.weiseer.com/scan?pkg=<package>"
```

The response is JSON with `verdict`, `score`, and a breakdown of each signal. You can parse this in a GitHub Action to block builds that attempt to install a malicious package.

## Integrating into a GitHub Action workflow

Here's a practical defense: add a step before `npm install` that scans every dependency in your `package.json`. If any package scores below 80, fail the build.

```yaml
- name: Scan dependencies with mcp-doctor
  run: |
    for pkg in $(jq -r '.dependencies | keys[]' package.json); do
      result=$(curl -s "https://api.weiseer.com/scan?pkg=$pkg")
      score=$(echo "$result" | jq '.score')
      if [ "$score" -lt 80 ]; then
        echo "BLOCKED: $pkg (score $score)"
        exit 1
      fi
    done
```

This catches supply-chain attacks before they reach your `node_modules`. The same pattern works for Python's `requirements.txt`.

## Why this matters for MCP specifically

MCP servers are uniquely dangerous because they execute arbitrary code on the host machine. The MCP protocol's tool-calling mechanism is essentially a remote code execution interface. A malicious MCP server can:

- Read and exfiltrate environment variables (API keys, model provider tokens).
- Access the filesystem (read/write model weights, training data).
- Execute shell commands via the `exec` tool pattern.
- Install additional malware as a postinstall script.

The Shai-Hulud worm exploited this by masquerading as a legitimate MCP server package. It spread through npm's dependency graph, infecting CI pipelines that auto-installed dependencies. The MCPwn CVEs showed that even without a worm, a single malicious MCP server could compromise an entire AI pipeline.

## The defense in practice

Your install-time gate should be the first line of defense. Run `mcp-doctor` on every new dependency before adding it to your project. For existing dependencies, re-scan periodically—a package that was safe yesterday might have been compromised today.

The tool's zero-auth, free API makes this practical for teams of any size. There's no onboarding, no API key management, no rate limiting for reasonable usage. Just a `curl` command or `npx` invocation.

## Limitations and complementary controls

No tool catches everything. `mcp-doctor` cannot detect a package that becomes malicious after installation (a "time-bomb" attack). For that, you need runtime monitoring and continuous scanning. The tool also cannot analyze obfuscated code—it relies on metadata signals.

Pair install-time gating with:

- **Runtime monitoring**: watch for unexpected network calls or file access from MCP servers.
- **Least privilege**: run MCP servers in containers with minimal permissions.
- **Dependency pinning**: use lockfiles and audit them.
- **Human deep-audit**: for production-critical packages, commission a manual code review.

The `mcp-doctor` tool is the first gate, not the only gate. But it's the gate that stops the worm before it enters your network.

_Free, zero-auth: scan any package now → curl "https://api.weiseer.com/scan?pkg=<package>" · CLI: `npx @weiseer/mcp-doctor <package>` · continuous monitoring (Pro): https://weiseer.gumroad.com/l/hxmty · human deep-audit for production sign-off: https://weiseer.gumroad.com/l/clrtzf_