#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import requests
import time

session_id_list = []
amount_list = []
question_number = []
questions = dict()
total_question_num = 0


def read_json():
    """
    :return: Nothing
    It reads the data.json file
    Stores in questions dictionary
    """
    with open("data.json", "r") as f:
        json_data = json.load(f)

    for i in range(len(json_data["results"])):
        questions[i] = json_data["results"][i]


def create_session_id(amount=10):
    """
    :param amount: Represents question amount. Default value is 10
    :return: Nothing
    """
    # If session_id_list is empty,
    # ID is assigned as 1 for starting session number
    if len(session_id_list) == 0:
        new_id = 1
        session_id_list.append(new_id)
        question_number.append(0)
        amount_list.append(amount)
    # If session_id_list is not empty,
    # last ID is incremented by 1 and added list
    else:
        new_id = session_id_list[-1]
        session_id_list.append(new_id+1)
        question_number.append(0)
        amount_list.append(amount)


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

    def new_game(self, query):
        amount = int(query["amount"][0])    # amount info is retrieved from query
        create_session_id(amount)           # new session is created
        self.send_response(200)
        self.end_headers()
        self.wfile.write(str.encode("New Trivia Game started\nSession ID = " + str(session_id_list[-1]) + "\n"))
        print("New Game Session ID: ", session_id_list[-1])  # debug print, it will be deleted

    def next(self, query):
        session_id = int(query["id"][0])        # Session id retrieved from query
        if session_id not in session_id_list:   # Session id is controlled
            self.wfile.write(str.encode("SessionID is unknown!\n"))
            return
        if question_number[session_id-1] == total_question_num:     # Total answered question number is checked
            self.wfile.write(str.encode("You answered the all questions!\nNo new question!\n"))
            return
        if amount_list[session_id-1] == question_number[session_id-1]:      # If total question is asked in related
            self.wfile.write(str.encode("You completed all questions!\n"))  # session, warning message is printed
            return
        self.send_response(200)
        self.end_headers()

        # Print on the command line
        self.wfile.write(str.encode("Question Number: " + str(question_number[session_id-1]+1) + "\n"))
        self.wfile.write(str.encode("Category: " + questions[question_number[session_id-1]]["category"] + "\n"))
        self.wfile.write(str.encode("Question: " + questions[question_number[session_id-1]]["question"] + "\n\n"))
        self.write_answers(question_number[session_id-1])
        self.wfile.write(str.encode("\nYou have 15 seconds to answer!\n"))
        question_number[session_id-1] += 1
        # TODO Call answer function
        print("START !!!!!!!")
        # start = self.date_time_string()
        start_ = self.log_date_time_string()
        finish_second = self.calculate_last_second(start_.split()[1])
        print(start_)
        print(finish_second)
        #print(start)
        # start = start.split()[4].split(":")[2]
        #print(start)

    def write_answers(self, number):
        """
        :param number: It represents question number
        :return: Nothing
        The function prints out the appropriate answer
        on the console
        """
        answers = [questions[number]["correct_answer"]]
        self.wfile.write(str.encode("- " + questions[number]["correct_answer"] + "\n"))
        for ans in questions[number]["incorrect_answers"]:
            self.wfile.write(str.encode("- " + ans + "\n"))

    def calculate_last_second(self, start_time):
        print(start_time)
        start_time = start_time.split(":")
        start_time =list(map(int, start_time))
        last_second = start_time[-1] + 15
        if last_second > 59:
            last_second = last_second - 60

        return last_second

    def do_GET(self):
        # Parse incoming request url
        print("GET")
        url = urlparse(self.path)
        print("\n", url, "\n")  # debug print
        if url.path == "/hello":
            return self.say_hello(parse_qs(url.query))
        elif url.path == "/newGame":
            return self.new_game(parse_qs(url.query))
            # return self.say_hello(parse_qs(url.query))
        elif url.path == "/next":
            return self.next(parse_qs(url.query))
        else:
            # return 404 code if path not found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found!\n')

    def do_POST(self):
        """
        There might be two different curl command. So, both of them should be handled
        to parse and retrieve answer. I used try-except structure here. In try part,
        I handled curl -d "id=xx&answer=xxxx" -X POST http://localhost:8080/answer
        In except part, I handled curl -X POST http://localhost:8080/answer\?id=xx\&answer=xxxx
        """

        print("POST")

        # TODO Parse curl command and get answer and id
        # TODO Add 15 seconds to answer. Hint: request.post(timeout=10)

        finish = self.date_time_string()
        finish = finish.split()[4].split(":")[2]
        #print(finish)
        finish_ = self.log_date_time_string()
        print(finish_)
        print(type(finish_))

        try:
            content_length = int(self.headers['Content-Length'])  # Gets the size of data
            post_data = self.rfile.read(content_length)  # Gets the data itself
            post_data = post_data.decode("ascii")   # decode the data from binary to string
            print(post_data.split("&"))
            post_data = post_data.split("&")        # string is split wrt '&'
            id = post_data[0].split("=")[1]         # id is split wrt '='
            answer = post_data[1].split("=")[1]     # id is split wrt '='
            print(id, answer)
        except TypeError:
            url = urlparse(self.path)
            print(parse_qs(url.query))


if __name__ == "__main__":
    # JSON data is read
    read_json()
    total_question_num = len(questions)
    print(total_question_num)
    port = 8080
    print(f'Listening on localhost:{port}')
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()
    # server.server_close()
