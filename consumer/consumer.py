"""
A simple http server to test as a webhook consumer

Will respond to any request with an empty body
and default response code 200 or the provided
response code to test failure cases.

The request path and body will be printed to stdout.

"""
import http.server
import socketserver
import sys

# TODO Use argParse with __main__
RESPONSE_CODE = int(sys.argv[1]) if len(sys.argv) > 1 else 200
HOST = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8888


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(RESPONSE_CODE)
        content_length = int(self.headers['Content-Length'])
        print("Received {} {} {}, Responded with {}".format(self.command, self.path,
                                                            self.rfile.read(content_length).decode(), RESPONSE_CODE))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("".encode())  # Empty response body for webhook

    def log_message(self, format, *args):
        return  # Suppress logging


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Starting webhook consumer at http://{}:{}/".format(HOST, PORT))
    httpd.serve_forever()
