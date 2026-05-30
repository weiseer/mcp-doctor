#!/usr/bin/env python3
"""
mcp-doctor scan HTTP endpoint.

Wraps scanner.scan_package() in a simple stdlib HTTP server with a permissive
CORS policy for the Node CLI + future web dashboard. Caches results 30 min per
package to limit upstream load and rate-limit per IP.

Listens on 127.0.0.1:8766. Nginx reverse-proxies to oracle.weiseer.com/mcp-doctor/.

License: Apache-2.0. Probe P-010.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from scanner import scan_package, ScanResult  # noqa: E402

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8766"))
CACHE_TTL_S = int(os.environ.get("CACHE_TTL_S", "1800"))  # 30 min
RATE_LIMIT_PER_IP_PER_MIN = int(os.environ.get("RATE_LIMIT_PER_IP_PER_MIN", "60"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [mcp-doctor-api] %(message)s")
log = logging.getLogger("mcp-doctor-api")

_cache: dict[str, tuple[float, dict]] = {}
_cache_lock = threading.Lock()
_rate: dict[str, list[float]] = {}
_rate_lock = threading.Lock()


def get_cached_or_scan(pkg: str) -> dict:
    now = time.time()
    with _cache_lock:
        hit = _cache.get(pkg)
        if hit and now - hit[0] < CACHE_TTL_S:
            return hit[1]
    result = scan_package(pkg)
    payload = asdict(result)
    with _cache_lock:
        _cache[pkg] = (now, payload)
    return payload


def check_rate_limit(ip: str) -> bool:
    now = time.time()
    cutoff = now - 60.0
    with _rate_lock:
        timestamps = _rate.setdefault(ip, [])
        timestamps[:] = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= RATE_LIMIT_PER_IP_PER_MIN:
            return False
        timestamps.append(now)
        return True


class H(BaseHTTPRequestHandler):
    server_version = "weiseer-mcp-doctor/0.1.0"

    def log_message(self, fmt, *args):
        log.info(f"{self.address_string()} {fmt % args}")

    def _send_json(self, status: int, payload: dict | list, headers: dict | None = None):
        body = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)
        path = u.path
        qs = parse_qs(u.query or "")

        client_ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()

        if path == "/health":
            self._send_json(200, {"status": "ok", "cached_entries": len(_cache)})
            return

        if path == "/scan":
            pkgs = qs.get("pkg", [])
            if not pkgs:
                self._send_json(400, {"error": "missing required query param `pkg`"})
                return
            if not check_rate_limit(client_ip):
                self._send_json(429, {"error": "rate limit: 60/min/IP"})
                return
            pkg = pkgs[0]
            try:
                result = get_cached_or_scan(pkg)
                self._send_json(200, result)
            except Exception as e:
                log.exception(f"scan_package failed for {pkg}")
                self._send_json(500, {"error": str(e), "package": pkg})
            return

        if path == "/badge":
            pkgs = qs.get("pkg", [])
            if not pkgs:
                self.send_response(404)
                self.end_headers()
                return
            try:
                result = get_cached_or_scan(pkgs[0])
            except Exception as e:
                self._send_json(500, {"error": str(e)})
                return
            verdict = result.get("verdict", "ERROR")
            score = result.get("score", 0)
            colors = {"PASS": "#3ddc7e", "WARN": "#f1b94a", "BLOCK": "#ef5350", "ERROR": "#888"}
            color = colors.get(verdict, "#888")
            label = "mcp-trust"
            value = f"{verdict} {score}"
            label_w = 70
            value_w = max(80, 10 * len(value) + 14)
            total_w = label_w + value_w
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20">'
                f'<linearGradient id="b" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>'
                f'<rect rx="3" width="{total_w}" height="20" fill="#555"/>'
                f'<rect rx="3" x="{label_w}" width="{value_w}" height="20" fill="{color}"/>'
                f'<rect rx="3" width="{total_w}" height="20" fill="url(#b)"/>'
                f'<g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,sans-serif" font-size="11">'
                f'<text x="{label_w // 2}" y="14">{label}</text>'
                f'<text x="{label_w + value_w // 2}" y="14">{value}</text>'
                f'</g></svg>'
            )
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "max-age=300")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(svg.encode("utf-8"))
            return

        self._send_json(404, {"error": "not found", "available_paths": ["/scan?pkg=", "/badge?pkg=", "/health"]})


def main():
    log.info(f"mcp-doctor-api listening on http://{HOST}:{PORT} (cache_ttl={CACHE_TTL_S}s, rate_limit={RATE_LIMIT_PER_IP_PER_MIN}/min/IP)")
    server = ThreadingHTTPServer((HOST, PORT), H)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("shutdown")


if __name__ == "__main__":
    main()
