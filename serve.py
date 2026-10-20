import http.server, functools, sys, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", "": "application/octet-stream"}
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()
host = sys.argv[1] if len(sys.argv) > 1 else "192.168.15.185"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8085
http.server.ThreadingHTTPServer((host, port), functools.partial(H, directory=ROOT)).serve_forever()
