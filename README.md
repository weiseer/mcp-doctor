# mcp-doctor

> Install-time trust gate for MCP servers. PASS / WARN / BLOCK + cited evidence.

Open-source supply-chain scanner for the MCP ecosystem.

## Use

```bash
npx @weiseer/mcp-doctor zod
npx @weiseer/mcp-doctor --config ~/.config/claude/claude_desktop_config.json
```

## Components

- [`rubric.yaml`](./rubric.yaml) — open-source trust scoring rubric (20+ signals)
- [`scanner.py`](./scanner.py) — Python scanner core (npm + OSV + GitHub API)
- [`http_endpoint.py`](./http_endpoint.py) — public HTTP API wrapper
- [`cli/`](./cli/) — `@weiseer/mcp-doctor` npm CLI
- [`action/`](./action/) — `weiseer/mcp-doctor-action@v1` GitHub Action

## Endpoint

Public scoring endpoint: `https://api.weiseer.com/scan?pkg=<package>`. Free tier: 60 req/min/IP, no auth.

## License

Apache-2.0
