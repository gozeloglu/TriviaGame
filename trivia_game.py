#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    def say_hello(self, query):
        """
        Send Hello Message with optional query
        """
        mes = "Hello"
        if "name" in query:
            # query is params are given as array to us
            mes += " " + "".join(query["name"])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode(mes+"\n"))

    def do_GET(self):
        # Parse incoming request url
        url = urlparse(self.path)
        if url.path == "/hello":
            return self.say_hello(parse_qs(url.query))
        # return 404 code if path not found
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found!\n')


if __name__ == "__main__":
    port = 8080
    print(f'Listening on localhost:{port}')
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
