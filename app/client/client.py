## Mods
import socket
from fl_networking_tools import get_binary, send_binary

'''
Responses
1 - Used to receive questions
2 - Used to confirm joined game
'''

## Waiting ?
waiting = True
## Playing ?
playing = False
## If stay to default, client will be kicked
pseudo = "default"

## Bind socket and connect to server
quiz_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quiz_server.connect(("127.0.0.1", 2065))

## Request to change pseudo
pseudo = input("Pseudo : ")

## Request for join
send_binary(quiz_server, ["JOIN", pseudo])

## Waiting loop
while waiting:
    for response in get_binary(quiz_server):
        if response[0] == 1:
            print(response[1])
        elif response[0] == 1:
            print(response[1])

playing = True
## Request for question
send_binary(quiz_server, ["QUESTION", ""])

## Playing loop
while playing:
    for response in get_binary(quiz_server):
        ## Show question
        if response[0] == 1:
            print(response[1])
            ## Ask for input
            answer = input("Type an answer : ")
            ## Send answer
            send_binary(quiz_server, ["ANSWER", answer])