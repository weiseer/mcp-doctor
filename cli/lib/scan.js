const ENDPOINT = process.env.MCP_DOCTOR_ENDPOINT || "https://api.weiseer.com/scan";
const LOCAL_FALLBACK = process.env.MCP_DOCTOR_LOCAL_FALLBACK === "1";

async function scanOnePackage(pkg) {
  const url = new URL(ENDPOINT);
  url.searchParams.set("pkg", pkg);
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 15000);
    const res = await fetch(url, { signal: ctrl.signal, headers: { "User-Agent": "weiseer-mcp-doctor-cli/0.1.2" } });
    clearTimeout(t);
    if (!res.ok) {
      return {
        package: pkg, version: "", verdict: "ERROR", score: 0,
        error: "endpoint http " + res.status,
        triggered_signals: [], metadata: {},
        scanned_at: new Date().toISOString(),
      };
    }
    return await res.json();
  } catch (e) {
    return {
      package: pkg, version: "", verdict: "ERROR", score: 0,
      error: "endpoint: " + e.message,
      triggered_signals: [], metadata: {},
      scanned_at: new Date().toISOString(),
    };
  }
}

export async function scanPackages(packages, opts = {}) {
  const results = [];
  for (const pkg of packages) {
    results.push(await scanOnePackage(pkg));
  }
  return results;
}
