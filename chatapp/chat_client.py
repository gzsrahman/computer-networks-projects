#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)

#!/usr/bin/python3
#
# COMP 332, Spring 2023
# Chat client
#
# Example usage:
#
#   python3 chat_client.py <chat_host> <chat_port>
#

import socket
import sys
import threading


class ChatClient:

    def __init__(self, chat_host, chat_port):
        self.chat_host = chat_host
        self.chat_port = chat_port
        self.start()

    def start(self):

        # Open connection to chat
        try:
            chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            chat_sock.connect((self.chat_host, self.chat_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ")
            if chat_sock:
                chat_sock.close()
            sys.exit(1)

        threading.Thread(target=self.write_sock, args=(chat_sock,)).start()
        threading.Thread(target=self.read_sock, args=(chat_sock,)).start()

    def write_sock(self, sock):
        # Feeling whimsical
        # Look at me letting you enter your name, truly tha goat
        name = input("Enter your name: ")

        # Nicifying the program by sending a message to other users when you
        # Enter da chatty chat
        intro = "[Entered]"
        lentro = len(intro.encode('utf-8'))
        hintroname = "name: " + name 
        hintrolen = "length: " + str(lentro)
        hintro = hintroname + "//" + hintrolen + "&headerendbaby&"
        intropack = hintro + intro 
        bintro = intropack.encode('utf-8')
        if len(name) == 0:
            bintro = b''
        sock.sendall(bintro)
        print(name + ": [Entered]")

        # Continuous yktv
        while True:

            # idk
            # print("In write_sock")

            # Get and print your message
            message = input("")
            # print("So you're sayin: " + message)

            # Figure out length of message in bytes
            length = len(message.encode('utf-8'))

            # Put together da header
            hname =  "name: " + name
            hlength = "length: " + str(length)
            header = hname + "//" + hlength
            header += "&headerendbaby&"

            # Making and sending da packet >:^D
            packet = header + message
            binpacket = packet.encode('utf-8')
            if len(message) == 0:
                binpacket = b''
            sock.sendall(binpacket)


    def read_sock(self, sock):
        while True:

            # Again, idk y'all added dis one
            #print("In read_sock")

            # Get da packet and decode da packet
            binpacket = sock.recv(4096)
            packet = binpacket.decode('utf-8')

            # Get header and message info from da packet
            # From the header, get the length and name info <3
            header, message = packet.split("&headerendbaby&")
            hname, hlength = header.split("//")

            # Let's clean up our info >:^D
            name = hname[6:]
            length = int(hlength[8:])

            # un fort you nate lee, you had to go and say we needed byte length
            # and now i gotta go and do this >:^(
            message = message.encode('utf-8')[:length].decode('utf-8')

            # Okay now I'm calm again :)
            print(name + ": " + message)

def main():

    print (sys.argv, len(sys.argv))
    chat_host = 'localhost'
    chat_port = 50008

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])

    chat_client = ChatClient(chat_host, chat_port)

if __name__ == '__main__':
    main()
