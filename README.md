# TriviaGame

## Motivation

I was curious about backend programming for a while. So, I decided to implement a basic Trivia Game by using Trivia game data. I implemented in `Python` without using any third-party library. In this stage, I used data in JSON format, not sending a request to the URL. I may extend this project like sending a request in real-time.



## Run

Firstly, clone project into your computer. Then, you need to go project directory. Run below command:

```
$ python3 trivia_game.py
```

`Python3` must be installed in your computer. I recommend you to open two terminal because program should be run during the game. While the program running in one terminal, you can send `curl` commands in the other terminal. 



## How to play

I used two different REST API method which are `GET` and `POST`. The `GET` method is used for creating a new game and retrieving questions. The `POST` method is used for answering the questions. There are two different curl command for POSTing answer. You can create more than one game session and play them concurrently. Each `newGame` request creates new game session.   



#### Create a new game

You need to send `GET`  request to create a new game. It takes one parameter which is the amount of the question of the game.

```
/newGame
METHOD: GET
Example: http://localhost:8080/newGame?amount=10
```

Example `curl` command:

```
$ curl http://localhost:8080/newGame?amount=10
New Trivia Game started
Session ID = 1
```

#### Get next question

You need to send `GET`request to get next question in given game session. It takes one parameter which is the game session id. If you use a game session id which is not created yet, you will get error with a message. Do not forget, you will have only 15 seconds to give answer! 



```
/next
METHOD: GET
Example: http://localhost:8080/next?id=1
```

Example `curl` commad:

```
$ curl http://localhost:8080/next?id=1
Question Number: 1
Category: General Knowledge
Question: Which sign of the zodiac is represented by the Crab?

Answers:
- Virgo
- Cancer
- Libra
- Sagittarius

You have 15 seconds to answer!

```

#### Answer Question

You need to send `POST` request to give answer the question for given session id. You can send two type of `curl` command for this operation. Again, do not forget, you will have only 15 seconds to give the answer to the question! If you exceed this time, your answer will not be accepted! It takes two parameters in the URL. The first one is session id, the second one is answer. 



```
/answer
METHOD: POST
Example: http://localhost:8080/answer
Example: http://localhost:8080/answer?id=1&answer=Cancer
```

Example `curl` commands: 

```
$ curl -d "id=1&answer=Cancer" -X POST http://localhost:8080/answer
CORRECT ANSWER!!

1 correct of 1 questions

There are 9 more questions

```

```
$ curl -X POST http://localhost:8080/answer?id=1&answer=Cancer
CORRECT ANSWER!!

1 correct of 1 questions

There are 9 more questions

```

#### Note

:warning: While answering the questions, if you are using this format

`curl -X POST http://localhost:8080/answer\?id\=1\&answer\=xxxxx` 

and your answer has more than 1 word, you need to put `-` middle of the each words.



### Future

I can use Trivia Game API to get data in real-time instead of JSON file.


