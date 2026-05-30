# @weiseer/mcp-doctor

> Install-time trust gate for MCP servers. PASS / WARN / BLOCK + cited evidence.

Part of [weiseer](https://github.com/weiseer). Probe **P-010**.

## What it does

Scans MCP server packages (or your entire `claude_desktop_config.json` / `cline_config.json`) and tells you which ones to trust before you install or connect to them.

Verdict is one of:
- **PASS** — no significant supply-chain or vulnerability signals
- **WARN** — material concerns; review before installing
- **BLOCK** — critical issue (known CVE, typosquat, hardcoded credentials, etc.)

All scoring is **open-source and rule-based** — see [rubric.yaml](./rubric.yaml). You can argue with our methodology; we'd rather you do that than trust a black-box ML model.

## Install

```bash
npm install -g @weiseer/mcp-doctor
```

Or run on-demand:

```bash
npx @weiseer/mcp-doctor @modelcontextprotocol/server-github
```

## Common uses

**1. Check a single package before installing:**

```bash
npx @weiseer/mcp-doctor @some/mcp-server
```

**2. Audit your existing MCP config:**

```bash
npx @weiseer/mcp-doctor --config ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**3. CI integration (block bad MCPs in PR):**

```yaml
- uses: weiseer/mcp-doctor-action@v1
  with:
    packages: '@x/server-foo @y/server-bar'
```

**4. README trust badge:**

```md
![MCP Trust](https://weiseer.com/badge/@x/server-foo)
```

## What gets scored

- **Supply chain hygiene** — postinstall scripts, unpinned deps, missing provenance, repo URL integrity
- **Maintainer health** — release cadence, archive status, bus factor, GitHub last-push age
- **Known vulnerabilities** — direct + transitive CVE via OSV.dev
- **MCP-specific risk** — typosquat against official servers, hardcoded credentials, capability misdeclaration

Full rubric: [rubric.yaml](./rubric.yaml). Open-source by design.

## Why this exists

The MCP ecosystem has a security crisis. MCPwn (CVE-2026-33032, CVSS 9.8) exposed 2,600+ instances. The Shai-Hulud npm worm stole MCP auth tokens from 172 packages. MCPSafe found high-severity bugs in *official* MCP servers from Atlassian, GitHub, Cloudflare, Microsoft. Bumblebee shipped from Perplexity in May 2026 specifically because supply-chain scanning was missing for MCP.

We agree the problem is real and decided to ship a developer-friendly install gate that fits the existing MCP workflow rather than reinventing it.

## License

Apache-2.0.

## Related

- Open-source rubric: [rubric.yaml](./rubric.yaml)
- 9 other weiseer MCP services: [github.com/weiseer](https://github.com/weiseer)
