#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)
#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2023
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>
#

# Python modules
import socket
import sys
import threading


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.web_cache = {}
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)

        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:
            client_conn, client_addr = proxy_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(
                    target = self.serve_content, args = (client_conn, client_addr))
            thread.start()

    def serve_content(self, client_conn, client_addr):

        # Todos
        # Receive request from client
        bin_req = client_conn.recv(4096)
        get_req = bin_req.decode('utf-8')
        print(get_req)
        
        # Find the hostname

        # The hostname starts 2 characters after the first colon
        hoststart = 0
        for i in range(len(get_req)):
            if get_req[i] == ':':
                hoststart = i + 2
                break
        # The hostname ends 2 characters before the second colon
        hostend = 0
        for i in range(len(get_req))[hoststart:]:
            if get_req[i] == ':':
                hostend = i-12
                break 
        
        host = get_req[hoststart:hostend]

        # Send request to web server
        try:
            web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            web_sock.connect((host, 80))

        except OSError as e:
            print ("Unable to open web socket: ", e)
            if web_sock:
                web_sock.close()
            sys.exit(1)

        # Wait for response from web server
        web_sock.sendall(bin_req)
        bin_resp = web_sock.recv(4096)

        # Send web server response to client
        client_conn.sendall(bin_resp)

        # Close connection to client
        client_conn.close()

def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50007

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
