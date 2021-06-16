## Mods
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary
from threading import Event

'''
Commands:
QUESTION - Used to request a question from the server
ANSWER - Used to send an answer to the server for feedback
JOIN - Used to request for join
'''

## Question model
Question = namedtuple('Question', ['q', 'answer'])
## Questions
q1 = Question("Expand the acronym ALU", "Arithmetic Logic Unit")

## MultiThread
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

REQUIRED_PLAYERS = 2
players_list = []
answers_total = 0

## Events
ready_to_start = Event()
wait_for_answers = Event()

## Socket handler class
class QuizGame(socketserver.BaseRequestHandler):
    def handle(self):
        global players_list
        ## Retrieve command from client
        for command in get_binary(self.request):
            if command[0] == "JOIN":
                ## Check if user has changed his name. If not, send a message
                if command[1] == "default":
                    todo
                else:
                    ## Retrieve pseudo and add it to players_list
                    pseudo = command[1]
                    players_list.append(pseudo)
                    ## Confirmation message
                    send_binary(self.request, [1, "Welcome in the networked quizz game !"])
                    ## Wait for start
                    ready_to_start.wait()
                ## Check if enough players
                if len(players_list) == REQUIRED_PLAYERS:
                    ## Game starting
                    send_binary(self.request, [1, "The game is about to start !"])
                    ## Trigger the event
                    ready_to_start.set()
            ## Send question
            elif command[0] == "QUESTION":
                send_binary(self.request, (1, q1.q))
            ## Retrieve answer
            elif command[0] == "ANSWER":
                answer = command[1]
                ## Check the answer
                if answer == q1.answer:
                    ## False
                    send_binary(self.request, (1, "True"))
                else:
                    ## True
                    send_binary(self.request, (1, "False"))

## Start server, bind socket
quiz_server = socketserver.ThreadingTCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()