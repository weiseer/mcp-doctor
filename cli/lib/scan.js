/**
 * Scan dispatcher for mcp-doctor CLI.
 *
 * v0.1 (Day 3): calls the public scoring endpoint at weiseer-mcp-doctor backend.
 * v0.2+ (Day 5): bundles trust DB + rubric for fully-offline scan.
 *
 * The hosted endpoint runs the same open-source rubric (rubric.yaml in this repo).
 * The endpoint is rate-limited free / no auth required, capped at 1000 calls/day/IP.
 */
const ENDPOINT = process.env.MCP_DOCTOR_ENDPOINT || "https://oracle.weiseer.com/mcp-doctor/scan";
const LOCAL_FALLBACK = process.env.MCP_DOCTOR_LOCAL_FALLBACK === "1";

async function scanOnePackage(pkg) {
  const url = new URL(ENDPOINT);
  url.searchParams.set("pkg", pkg);
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const res = await fetch(url, { signal: ctrl.signal, headers: { "User-Agent": "weiseer-mcp-doctor-cli/0.1.0" } });
    clearTimeout(t);
    if (!res.ok) {
      return {
        package: pkg, version: "", verdict: "ERROR", score: 0,
        error: `endpoint http ${res.status}`,
        triggered_signals: [], metadata: {},
        scanned_at: new Date().toISOString(),
      };
    }
    return await res.json();
  } catch (e) {
    return {
      package: pkg, version: "", verdict: "ERROR", score: 0,
      error: `endpoint unreachable: ${e.message}`,
      triggered_signals: [], metadata: {},
      scanned_at: new Date().toISOString(),
    };
  }
}

export async function scanPackages(packages, opts = {}) {
  const results = [];
  // Sequential for now; the rate-limit per IP is generous but we are polite.
  for (const pkg of packages) {
    results.push(await scanOnePackage(pkg));
  }
  return results;
}
