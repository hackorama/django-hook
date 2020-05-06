"""
A simple HTTP server to test as a webhook consumer.

Will respond to any POST request with an empty body
and default response code 200 or the provided
response code to test failure cases.

The POST request path and body will be printed to stdout.

Any GET request will list the n most recent webhook POST
calls received by this consumer in reverse order.

"""
import http.server
import socketserver
import sys
from collections import deque

# TODO Use argParse with __main__
RESPONSE_CODE = int(sys.argv[1]) if len(sys.argv) > 1 else 200
HOST = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
PORT = int(sys.argv[3]) if len(sys.argv) > 3 else 8888
MAX_CALL_LOGS = 20


class Handler(http.server.SimpleHTTPRequestHandler):
    call_log = deque(maxlen=MAX_CALL_LOGS)  # Track the last n web hook calls

    def do_GET(self):
        # Displays the most recent webhook call list
        self.send_response(RESPONSE_CODE)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if len(self.call_log) < 1:
            self.wfile.write("No webhook calls received by this consumer".encode())
        else:
            self.wfile.write("Webhook calls received by this consumer".encode())
            self.wfile.write("<br>".encode())
            self.wfile.write("<table border=1>".encode())
            self.wfile.write("<tr><th>Webhook path</th><th>Payload</th></tr>".encode())
            for call in reversed(self.call_log):
                self.wfile.write(call.encode())
            self.wfile.write("</table>".encode())
            self.wfile.write(
                "<i>Listed in reverse order, limited to most recent {}</i>".format(self.call_log.maxlen).encode())

    def do_POST(self):
        # Log and add the web hook call to the webhook call log list
        # and respond with configured response code and empty body
        self.send_response(RESPONSE_CODE)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        print("Received {} {} {}, Responded with {}".format(self.command, self.path, body, RESPONSE_CODE))
        self.call_log.append("<tr><td>{}</td><td>{}</td></tr>".format(self.path, body))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("".encode())  # Empty response body as expected for webhook

    def log_message(self, format, *args):
        return  # Suppress internal logging from http.server for development demo brevity


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Starting webhook consumer at http://{}:{}/".format(HOST, PORT))
    httpd.serve_forever()
