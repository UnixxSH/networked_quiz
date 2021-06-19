## Mods
import socket
from fl_networking_tools import get_binary, send_binary

'''
Responses
1 - Used to receive questions and feedback
2 - Used to confirm joined game
3 - Used to check question availability
'''

## Waiting ?
waiting = True
## Playing ?
playing = False

## Bind socket and connect to server
quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quiz_server.connect(("127.0.0.1", 2065))

## Request to change pseudo
pseudo = input("Pseudo : ")

## Request for join
send_binary(quiz_server, ["JOIN", pseudo])

playing = True

## Playing loop
while playing:
    for response in get_binary(quiz_server):
        ## Show question
        if response[0] == 1:
            print(response[1])
        ## Request for question availability
        elif response[0] == 2:
            print(response[1])
            send_binary(quiz_server, ["STAT", ""])
        ## Request for question
        elif response[0] == 3:
            print(response[1])
            send_binary(quiz_server, ["QUESTION", ""])
        ## Show question
        elif response[0] == 4:
            print(response[1])
            ## Ask for input
            answer = input("Type an answer : ")
            ## Send answer
            send_binary(quiz_server, ["ANSWER", answer])