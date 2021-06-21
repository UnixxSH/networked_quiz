## Mods
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary
from threading import Event
from random import choice

'''
Commands:
QUESTION - Used to request a question from the server
ANSWER - Used to send an answer to the server for feedback
JOIN - Used to request for join
STAT - Used to retrieve quizz status
'''

## Question model
Question = namedtuple('Question', ['q', 'answer'])
## Questions
quiz_questions = [
    Question("Expand the acronym ALU", "Arithmetic Logic Unit"),
    Question("What does RAM stand for?", "Random Access Memory")
]

## MultiThread
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

## Variables
required_players = 2
players_list = []
answers_total = 0
current_question = None
scores = {}

## Events
ready_to_start = Event()
wait_for_answers = Event()

## Socket handler class
class QuizGame(socketserver.BaseRequestHandler):
    def handle(self):
        global players_list, answers_total, current_question, scores
        ## Retrieve command from client
        for command in get_binary(self.request):
            if command[0] == "JOIN":
                ## Retrieve pseudo and add it to players_list
                pseudo = command[1]
                players_list.append(pseudo)
                ## Set score to 0
                scores[pseudo] = 0
                ## Confirmation message
                send_binary(self.request, [2, "Welcome in the networked quizz game !"])
                ## Check if enough players
                if len(players_list) == required_players:
                    ## Trigger the event
                    ready_to_start.set()
                ## Wait until players
                ready_to_start.wait()
            ## Send question
            elif command[0] == "QUESTION":
                ## Select question randomly
                if current_question == None:
                    current_question = choice(quiz_questions)
                    wait_for_answers.clear()
                send_binary(self.request, (4, current_question.q))
            ## Retrieve answer
            elif command[0] == "ANSWER":
                answer = command[1]
                ## Check the answer
                answers_total += 1
                ## Wait for others players to answer
                if answers_total == len(players_list):
                    wait_for_answers.set()
                wait_for_answers.wait()
                if answer == current_question.answer:
                    ## True
                    scores[pseudo] += 1
                    send_binary(self.request, (5, scores[pseudo]))
                else:
                    ## False
                    send_binary(self.request, (6, scores[pseudo]))
                ## Remove question from list
                quiz_questions.remove(current_question)
                current_question = None
            ## Check if quizz is starting or continuing
            elif command[0] == "STAT":
                if ready_to_start.is_set() and not wait_for_answers.is_set():
                    send_binary(self.request, [3, "Quiz is starting"])
                elif ready_to_start.is_set() and wait_for_answers.is_set():
                    send_binary(self.request, [3, "Next question"])

## Start server, bind socket
quiz_server = socketserver.ThreadingTCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()