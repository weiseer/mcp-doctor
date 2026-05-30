#!/usr/bin/env node
/**
 * @weiseer/mcp-doctor — install-time trust gate CLI for MCP servers.
 * v0.1.0 — Day 3 ship.
 *
 * Usage:
 *   npx @weiseer/mcp-doctor <package1> [<package2> ...]
 *   npx @weiseer/mcp-doctor --config /path/to/claude_desktop_config.json
 *   npx @weiseer/mcp-doctor --json
 *
 * Exits non-zero on any BLOCK — useful for CI integration.
 * License: Apache-2.0. P-010.
 */
import { scanPackages } from "../lib/scan.js";
import { readFileSync } from "node:fs";
import { argv, exit, stderr } from "node:process";

function parseArgs(args) {
  const out = { packages: [], json: false, configPath: null, registry: null };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === "--json") out.json = true;
    else if (a === "--config") { out.configPath = args[++i]; }
    else if (a === "--registry") { out.registry = args[++i]; }
    else if (a === "--help" || a === "-h") {
      printHelp();
      exit(0);
    } else if (a.startsWith("--")) {
      stderr.write(`unknown flag: ${a}\n`);
      exit(2);
    } else {
      out.packages.push(a);
    }
  }
  return out;
}

function printHelp() {
  const txt = `mcp-doctor — install-time trust gate for MCP servers.

USAGE
  mcp-doctor <package1> [<package2> ...]
  mcp-doctor --config <path-to-claude_desktop_config.json>
  mcp-doctor --json

Open-source rubric: https://github.com/weiseer/mcp-doctor/blob/main/rubric.yaml

EXIT CODES
  0 = all PASS or WARN
  1 = at least one BLOCK
  2 = invalid usage
`;
  process.stdout.write(txt);
}

function packagesFromConfig(configPath) {
  const raw = JSON.parse(readFileSync(configPath, "utf-8"));
  const mcpServers = raw.mcpServers || {};
  const pkgs = new Set();
  for (const [, srv] of Object.entries(mcpServers)) {
    // Detect npx -y <pkg> args
    if (srv.command === "npx") {
      const args = srv.args || [];
      // skip -y flags, pick first non-flag arg
      for (const a of args) {
        if (a.startsWith("-")) continue;
        pkgs.add(a);
        break;
      }
    }
  }
  return [...pkgs];
}

function emoji(v) {
  return ({ PASS: "✓", WARN: "⚠", BLOCK: "✗", ERROR: "?" })[v] || "?";
}

function renderHuman(r) {
  const head = `${emoji(r.verdict)} ${r.verdict}: ${r.package}@${r.version || "?"}  (score ${r.score}/100)${r.self_disclosure ? " [self-disclosed]" : ""}`;
  if (r.error) return head + `\n  ERROR: ${r.error}`;
  const sigs = (r.triggered_signals || []).map(s => `    -${s.deduct}${s.hard_block ? " HARD" : ""} ${s.signal_id}: ${s.evidence}`);
  const m = r.metadata || {};
  const tail = `  m=${m.maintainer_count} dsr=${m.days_since_release} gh_dsp=${m.github_days_since_push} stars=${m.github_stars} deps=${m.dep_count} osv=${m.osv_vuln_count} lic=${m.license}`;
  return [head, ...sigs, tail].join("\n");
}

async function main() {
  const args = parseArgs(argv.slice(2));
  let packages = args.packages.slice();

  if (args.configPath) {
    try {
      packages = packages.concat(packagesFromConfig(args.configPath));
    } catch (e) {
      stderr.write(`config parse failed: ${e.message}\n`);
      exit(2);
    }
  }

  if (packages.length === 0) {
    printHelp();
    exit(2);
  }

  // Day 3 strategy: scanner is the Python engine. For v0.1 ship, the Node CLI
  // either (a) executes a hosted endpoint or (b) wraps a bundled scanning core.
  // Day 3 takes the simplest correct path: call the public scoring endpoint.
  //
  // For users who want fully-offline: --registry file:///path/to/bundled-db.json
  // will land in Day 5.
  const results = await scanPackages(packages, { registry: args.registry });

  if (args.json) {
    process.stdout.write(JSON.stringify(results, null, 2) + "\n");
  } else {
    for (const r of results) {
      process.stdout.write(renderHuman(r) + "\n\n");
    }
    const counts = results.reduce((acc, r) => { acc[r.verdict] = (acc[r.verdict] || 0) + 1; return acc; }, {});
    process.stdout.write(`summary: ${JSON.stringify(counts)}\n`);
  }

  if (results.some(r => r.verdict === "BLOCK")) exit(1);
}

main().catch(err => {
  stderr.write(`mcp-doctor: fatal: ${err.message}\n`);
  exit(2);
});
