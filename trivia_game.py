#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from random import randint

session_id_list = []


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

    def new_game(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode("New Trivia Game started\nSession ID = " + str(session_id_list[-1]) + "\n"))
        print("New Game Session ID: ", session_id_list[-1])  # debug print

    def do_GET(self):
        # Parse incoming request url
        url = urlparse(self.path)
        print("\n", url, "\n")  # debug print
        if url.path == "/hello":
            return self.say_hello(parse_qs(url.query))
        elif url.path == "/newGame":
            self.create_session_id()
            self.new_game()
            #return self.say_hello(parse_qs(url.query))
        else:
            # return 404 code if path not found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found!\n')

    def create_session_id(self):
        if len(session_id_list) == 0:
            new_id = 1
            session_id_list.append(new_id)
        else:
            new_id = session_id_list[-1]
            session_id_list.append(new_id+1)


if __name__ == "__main__":
    port = 8080
    print(f'Listening on localhost:{port}')
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
    server.server_close()
