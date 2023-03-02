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
import threading

from tictactoe import *

class Server():
    """
    Server for TicTacToe game
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 1
        self.start()

    def start(self):
        # Init server socket to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.host, self.port))
            server_sock.listen(self.backlog)
        except OSError as e:
            print ("Unable to open server socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)

        # Wait for client connection
        while True:
            client_conn, client_addr = server_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(target = self.play, args = (client_conn, client_addr))
            thread.start()

    def play(self, conn, addr):

        # Let's get the dimensions from the client, whose game has already started by now
        dimensions = sock_read(conn)
        dimensions = int(dimensions)

        # We'll make a tictactoe board of those dimensions (obviously)
        t = TicTacToe(dimensions)

        # Okay let's print into and declare the dimensions to the server
        t.printIntro()
        print("How many rows/columns would you like to play with? " + str(t.n))


        # This assignment is somehow hilarious to me
        # Choosing who goes first

        # For some reason I was having a hard time communicating booleans so this was
        # my last resort :(
        first = sock_read(conn)
        if first == "a":
            first = True 
        else:
            first = False
        if first == True:
            print("Alright, player. You will move first.")
        else:
            print("Yay! I will go first")

        # If not first, then computer gets initial move and sends move
        turn = 0
        if not first:
            t.printBreak()
            turn += 1
            print("Turn " + str(turn) + ":")
            move = t.compMove()
            sock_write(conn, str(move))

        # Now let's loop until the game is done
        while not t.board.checkWin():

            # Spacing
            t.printBreak()

            # Update turn count
            turn += 1
            print("Turn " + str(turn) + ":")

            # Receive player move from client
            move = sock_read(conn)
            move = t.toTuple(move)

            # I want both screens to show the same thing so this is what these print
            # statements are trying to do
            print("Please enter the row for your intended coordinates from 0-" + \
                str(t.n-1) + ": " + str(move[0]))
            print("Please enter the column for your intended coordinates from 0-" + \
                str(t.n-1) + ": " + str(move[1]))
            t.manualPlayer(move)
            
            # If the game is over then we'll return :/
            if t.board.checkWin():
                print(t.board.checkWin())
                print("Well played player!")
                return
            
            # If that didn't end the game let's keep going
            t.printBreak()
            turn += 1
            print("Turn " + str(turn) + ":")

            # Let's get the computer move and communicate it
            move = t.compMove()
            sock_write(conn, str(move))

        # If the player didn't win then yktv
        # Comp won playing randomly lol
        print(t.board.checkWin())
        print("Yay me!")
        return    

def main():

    server_host = 'localhost'
    server_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    s = Server(server_host, server_port)

if __name__ == '__main__':
    main()
