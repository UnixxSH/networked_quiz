## Mods
import socketserver
from collections import namedtuple
from fl_networking_tools import get_binary, send_binary

'''
Commands:
PLACE YOUR COMMANDS HERE
QUESTION - Used to request a question from the server
'''

## Question model
Question = namedtuple('Question', ['q', 'answer'])

## Questions
q1 = Question("Expand the acronym ALU", "Arithmetic Logic Unit")

## Handler socket class
class QuizGame(socketserver.BaseRequestHandler):
    def handle(self):
        for command in get_binary(self.request):
            if command[0] == "QUESTION":
                send_binary(self.request, (1, q1.q))

## Start server, bind socket
quiz_server = socketserver.TCPServer(('127.0.0.1', 2065), QuizGame)
quiz_server.serve_forever()