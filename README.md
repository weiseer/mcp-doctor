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


---

## 🆕 Fixed-price audit service (delivered in 24-48h)

If you would rather have a human-reviewed report than wire up the CLI yourself:

- **Single MCP audit — $49**: One package, deep-scanned, 1-page PDF verdict in 24h. [Buy on Gumroad](https://weiseer.gumroad.com)
- **Full agent supply-chain audit — $299**: Your entire MCP config scanned, 5-page PDF report + 30min Q&A in 48h. [Buy on Gumroad](https://weiseer.gumroad.com)

(The open-source CLI + free public API stays the same. The audit is for teams who want a fixed-price written deliverable for compliance / due-diligence purposes.)

---



## 🤝 Companion products (same author)

Full AI agent QA + safety stack:

- **mcp-doctor** (this repo) - install-time MCP supply-chain trust scanner
- **prompt-redteam** - github.com/weiseer/prompt-redteam - open-source jailbreak / prompt-injection tester (30+ patterns)
- **AI Agent QA Eval Pack** - 23 YAML test cases for tool-using agents across 6 failure dimensions (accuracy / safety / edge cases / prompt injection / hallucination / cost efficiency). Vendor-agnostic, no SDK migration. 9 at weiseer.gumroad.com/l/dcipxt

mcp-doctor checks what you install. prompt-redteam checks what you say. eval-pack checks what your agent loop does.

