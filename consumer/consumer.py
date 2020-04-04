import http.server
import socketserver
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8888


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        print("Received %s %s %s" % (self.command, self.path, self.rfile.read(content_length).decode()))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("".encode())  # Empty response body for webhook

    def log_message(self, format, *args):
        return  # Suppress logging


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Starting webhook consumer on http://%s:%d ..." % (HOST, PORT))
    httpd.serve_forever()
