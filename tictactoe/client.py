#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)
#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2023
# Homework 2: Distributed tic-tac-toe game

import binascii
import random
import socket
import sys

from tictactoe import *

class Client:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.start()

    def start(self):
        
        # Mostly used the echo_client code as the template for this but basically
        # We try to create the socket and specify the host/port
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((self.server_host, self.server_port))
        # If we can't initialize the socket then we return an error
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)
        # We'll only have gotten here if we initialized the socket, which means we're
        # good to go

        # Let's play >:)
        self.play(server_sock)

        # When we're done tho let's close
        server_sock.close()

    def play(self, sock):

        # A lot of this stuff is just gonna be recycled from my original code lol
        t = TicTacToe(3)
        t.printIntro()
        t.askDimensions()

        # Okay, we asked for the dimensions, now let's communicate them to the server
        # It's actually kinda funny when you think about it
        # The server doesn't even need to communicate lowkey?
        # I mean I already automated the server move in the original code
        # How would a normal unsuspecting person know if there were no server connect >:(
        # If this weren't a learning opportunity this assignment would make no sense
        sock_write(sock, str(t.n))

        # Client machine chooses who goes first and communicates that to server
        first = t.chooseFirst()

        # I was having a hard time communicating booleans so this was my final option lol
        if first:
            sock_write(sock, "a")
        else:
            sock_write(sock, "b")

        # Creating turn count lol
        turn = 0

        # If client is not first, then we receive the computer move from the server
        if not first:
            t.printBreak()
            turn += 1
            print("Turn " + str(turn) + ":")
            move = sock_read(sock)
            move = t.toTuple(move)
            t.manualComp(move)

        # With the first (or not) move out of the way, we loop until the game ends
        while not t.board.checkWin():
            
            # Spacing
            t.printBreak()

            # Update turn count from either 0 or 1
            turn += 1
            print("Turn " + str(turn) + ":")

            # Asking player what their move is and sending to server
            move = t.playerMove()
            sock_write(sock, str(move))

            # If the game has ended, then we break the loop
            if t.board.checkWin():
                print(t.board.checkWin())
                print("Well played player!")
                return

            # If the game hasn't ended, we proceed and update the turn count
            t.printBreak()
            turn += 1
            print("Turn " + str(turn) + ":")

            # Let's get the move info from the player and keep it pushing
            move = sock_read(sock)
            move = t.toTuple(move)
            t.manualComp(move)

        # If the player win condition didn't set off then the computer won, so let's
        # print accordingly
        print(t.board.checkWin())
        print("Yay me!")
        return


def main():
    server_host = 'localhost'
    server_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    client = Client(server_host, server_port)

if __name__ == '__main__':
    main()
