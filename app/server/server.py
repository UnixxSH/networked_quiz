## Mods
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary

'''
Commands:
QUESTION - Used to request a question from the server
'''
## Question model
Question = namedtuple('Question', ['q', 'answer'])

q1 = Question("Expand the acronym ALU", "Arithmetic Logic Unit")

## Socket handler class
class QuizGame(socketserver.BaseRequestHandler):
    def handle(self):
        ## Retrieve command from client
        for command in get_binary(self.request):
            ## Send question
            if command[0] == "QUESTION":
                send_binary(self.request, (1, q1.q))
            ## Retrieve answer
            if command[0] == "ANSWER":
                answer = command[1]
                if answer == q1.answer:
                    send_binary(self.request, (1, "True"))
                else:
                    send_binary(self.request, (1, "False"))

## Start server, bind socket
quiz_server = socketserver.TCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()