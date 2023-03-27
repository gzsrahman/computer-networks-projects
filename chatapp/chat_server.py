#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)

#!/usr/bin/python3
#
# COMP 332, Spring 2023
# Chat server
#
# Usage:
#   python3 chat_server.py <host> <port>
#

import socket
import sys
import threading

class ChatProxy():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_backlog = 1
        self.chat_list = {}
        self.chat_id = 0
        self.lock = threading.Lock()
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.server_host, self.server_port))
            server_sock.listen(self.server_backlog)
        except OSError as e:
            print ("Unable to open server socket")
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Wait for user connection
        while True:
            conn, addr = server_sock.accept()
            self.add_user(conn, addr)
            thread = threading.Thread(target = self.serve_user,
                    args = (conn, addr, self.chat_id))
            thread.start()

    def add_user(self, conn, addr):
        # print ('User has connected', addr)
        self.chat_id = self.chat_id + 1
        self.lock.acquire()
        self.chat_list[self.chat_id] = (conn, addr)
        self.lock.release()

    def getPackInfo(self, binpacket):
        
        # Use binpacket, not pre-decoded packet
        packet = binpacket.decode('utf-8')

        # Get packet info
        header, message = packet.split("&headerendbaby&")
        
        # Parse info
        hname, hlength = header.split("//")
        name = hname[6:]
        length = int(hlength[8:])

        # Return useful info
        return name, length, message

    def makePack(self, name, message):
        
        # Measure length of message
        length = len(message.encode('utf-8'))

        # Create header
        hname = "name: " + name 
        hlength = "length: " + str(length)
        header = hname + "//" + hlength + "&headerendbaby&"

        # Create and return packet
        packet = header + message
        return packet

    def read_data(self, conn):

        # Fill this out
        # print("In read data")

        # Get da packet, decode da packet >:)
        binpacket = conn.recv(4096)

        # If it's empty let's return something that indicates this
        if binpacket == b'':
            # message = "I'm leavin mayne"
            # packet = self.makePack(name, message)
            # print(name + ": " + message)
            return "$exitman$"
        
        # Get da information
        name, length, message = self.getPackInfo(binpacket)

        # This is for design, not functionality
        # Basically if this is a new user, I'll register their name
        # This way I can specify who left if they leave
        for key in self.chat_list.keys():
            if self.chat_list[key][0] == conn:
                if self.chat_list[key][-1] != name:
                    conn, addr = self.chat_list[key]
                    self.chat_list[key] = (conn, addr, name)
        
        # If we didn't get da full mensaje
        binmess = message.encode('utf-8')
        while len(binmess) < length:

            # Get da rest of da mensaje
            binpacket = conn.recv(4096)

            # Parse packet
            packet = packet.decode('utf-8')
            parts = packet.split("&headerendbaby&")

            # I'm not sure if getting another packet would include the
            # header so i'm playing it safe with the [-1] lol
            binmess += parts[-1].encode('utf-8')

            # Cut at appropriate length
            binmess = binmess[:length]
            message = binmess.decode('utf-8')

        # Okay, if the person hasn't left and if we got the full message
        message = message.encode('utf-8')[:length].decode('utf-8')
        packet = self.makePack(name, message)
        
        # The server prints to keep a log of all the chats, then returns
        print(name + ": " + message)
        return packet

    def send_data(self, user, data):
        self.lock.acquire()

        # Turn packet to binary, send for every user on the chat list
        # except for the specified sender
        binpacket = data.encode('utf-8')
        for key in self.chat_list.keys():
            if key != user:
                if len(self.chat_list[key]) == 3:
                    conn, addr, name = self.chat_list[key]
                else:
                    conn, addr = self.chat_list[key]
                conn.sendall(binpacket)

        self.lock.release()

    def cleanup(self, conn):
        self.lock.acquire()

        # Closing the connection and finding who left
        # print("In cleanup")
        conn.close()
        for key in self.chat_list.keys():
            if self.chat_list[key][0] == conn:
                break
        
        # If the person is in the list, we can output their name
        # when specifying who left
        inlist = False
        if len(self.chat_list[key]) == 3:
            name = self.chat_list[key][2]
            print(name + ": [Left]")
            inlist = True
        
        # Let's remove the user
        del self.chat_list[key]

        
        # Let's start making a packet to notify other users
        exitmess = "[Left]"
        hlength = "length: " + str(len(exitmess))
        if inlist:
            hname = "name: " + name 

        # If we don't know the person's name we'll specify by ID
        else:
            hname = "name: UserID[" + str(key) + "]"

        # Finish making da packet
        header = hname + "//" + hlength + "&headerendbaby&"
        packet = header + exitmess
        binpacket = packet.encode('utf-8')

        # Something about send_data didn't wanna cooperate so we'll
        # do this manually
        for key in self.chat_list.keys():
            if len(self.chat_list[key]) == 3:
                conn, addr, name = self.chat_list[key]
            else:
                conn, addr = self.chat_list[key]
            conn.sendall(binpacket)

        self.lock.release()

    def serve_user(self, conn, addr, user):

        # Fill this out
        # print("In serve user")

        # Continuously serve users
        while True:
        
            # Get da packet
            packet = self.read_data(conn)
            
            # If it says the person is leaving, break da loop
            if packet == "$exitman$":
                break

            # Otherwise send data and continue serving
            self.send_data(user, packet)

        # If we've broken the loop it's time to close the connection
        # Sad, R.I.P. :(((
        self.cleanup(conn)


def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    chat_server = ChatProxy(server_host, server_port)

if __name__ == '__main__':
    main()
