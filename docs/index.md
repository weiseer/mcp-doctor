---
layout: default
title: "mcp-doctor — check any MCP server before you install it"
---

# mcp-doctor — install-time MCP supply-chain trust gate

Free, zero-auth. Scan any npm/MCP package: `npx @weiseer/mcp-doctor <package>` or `curl "https://api.weiseer.com/scan?pkg=<package>"`. PASS / WARN / BLOCK with cited evidence.

## Guides

- [How to check if an npm/MCP package ships a hardcoded API key](g/check-npm-package-hardcoded-api-key)
- [An install-time trust gate for MCP servers: PASS / WARN / BLOCK explained](g/install-time-trust-gate-mcp-pass-warn-block)
- [How to audit every MCP server in your AI agent stack](g/audit-mcp-servers-in-your-agent-stack)
- [MCP supply-chain attacks (Shai-Hulud, MCPwn): defending at install time](g/mcp-supply-chain-attack-defend-install-time)
- [How to gate MCP servers in CI with a free GitHub Action](g/gate-mcp-servers-in-ci-github-action)
- [How to detect a typosquatted MCP server on npm](g/detect-typosquat-mcp-server-npm)
- [How to spot an abandoned or unmaintained MCP server](g/spot-abandoned-unmaintained-mcp-server)
- [Is an MCP server safe to install? How to check before you add it](g/is-an-mcp-server-safe-to-install-how-to-check)
