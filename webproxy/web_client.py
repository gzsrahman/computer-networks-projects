#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)
#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2023
# Homework 3: Simple web client to interact with proxy
#
# Example usage:
#
#   python3 web_client.py <proxy_host> <proxy_port> <requested_url>

# Python modules
import binascii
import socket
import sys

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url
        self.start()

    def start(self):

        # Open connection to proxy
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.connect((self.proxy_host, self.proxy_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Send requested URL to proxy

        # Break down url; everything before the first slash specifies the host
        # and everything after specifies the path
        url = self.url
        slashcount = 0
        thirdslash = 0
        for i in range(len(url)):
            if url[i] == '/':
                slashcount += 1
                if slashcount == 3:
                    thirdslash = i
        
        # Base case building a hostname and path
        hostname = self.url
        path = '/'

        # If first slash is 0 then there is no specified path, so we keep the default
        # hostname and path
        # Otherwise, we can use the location of the first slash to get the hostname and
        # path like we discussed before
        if slashcount > 2:
            hostname = url[:thirdslash]
            path = url[thirdslash:]

        # Getting rid of the http://
        hostname = hostname[7:]
            
        # Now we'll set up a get request using a persistent HTTP connection
        get_req = "GET " + path + " HTTP/1.1\r\nHost: " + hostname + "\r\n"
        get_req += "Connection: close\r\n\r\n"

        # Convert to binary
        bin_req = get_req.encode('utf-8')

        # Let's send the binary get request to the proxy
        proxy_sock.sendall(bin_req)

        # Receive binary data from proxy
        bindata = proxy_sock.recv(4096)

        # Decode bindata
        data = bindata.decode('utf-8')

        # Printing the data that we got back from the proxy
        print(data)

        proxy_sock.close()

def main():

    print (sys.argv, len(sys.argv))
    proxy_host = 'localhost'
    proxy_port = 50007
    url = 'http://example.com/'
    #url = 'http://eu.httpbin.org'
    #url = 'http://info.cern.ch/'
    #url = 'http://www-db.deis.unibo.it/'

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)

if __name__ == '__main__':
    main()
