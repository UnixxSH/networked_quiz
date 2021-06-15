## Mods
import socket
from fl_networking_tools import get_binary, send_binary

'''
Responses
1 - Question
'''

## Playing ?
playing = True

## Bind socket and connect to server
quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quiz_server.connect(("127.0.0.1", 2065))

## Request for question
send_binary(quiz_server, ["QUESTION", ""])

while playing:
    for response in get_binary(quiz_server):
        ## Show question
        if response[0] == 1:
            print(response[1])
            ## Ask for input
            answer = input("Type an answer : ")
            ## Send answer
            send_binary(quiz_server, ["ANSWER", answer])