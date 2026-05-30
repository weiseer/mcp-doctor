# mcp-doctor-action

> GitHub Action to block dangerous MCP server installs in CI.

Part of [weiseer](https://github.com/weiseer). Wraps [`@weiseer/mcp-doctor`](https://www.npmjs.com/package/@weiseer/mcp-doctor) CLI for GitHub Actions workflows.

## Usage

```yaml
name: MCP Trust Check
on: [pull_request, push]

jobs:
  mcp-doctor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: weiseer/mcp-doctor-action@v1
        with:
          # Option A: explicit package list
          packages: '@x/server-foo @y/server-bar'

          # Option B: scan your MCP config file
          config-path: '.mcp/claude_desktop_config.json'

          # Failure policy: strict (any WARN+), block-only (default), report (never fail)
          policy: 'block-only'
```

## Inputs

| Name | Required | Default | Description |
|---|---|---|---|
| `packages` | one of | — | Space-separated npm packages to scan |
| `config-path` | one of | — | Path to MCP config JSON to scan |
| `policy` | no | `block-only` | Failure threshold |
| `endpoint` | no | api.weiseer.com | Custom scan endpoint |

## Outputs

- `results` — JSON array of scan results
- `summary` — Markdown summary (also written to job summary)

## Example: Block PRs that add risky MCPs

```yaml
on: pull_request
jobs:
  guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: weiseer/mcp-doctor-action@v1
        with:
          config-path: 'apps/cli/mcp.config.json'
          policy: 'strict'
```

## License

Apache-2.0.
