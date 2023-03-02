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

# Python modules
import socket
import sys
import threading

# Project modules
import http_constants as const
import http_util


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.cache = {}
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
            conn, addr = proxy_sock.accept()
            print ('Client has connected', addr)
            thread = threading.Thread(target = self.serve_content, args = (conn, addr))
            thread.start()

    def serve_content(self, conn, addr):

        # Receive binary request from client
        bin_req = conn.recv(4096)
        try:
            str_req = bin_req.decode('utf-8')
            print(str_req)
        except ValueError as e:
            print ("Unable to decode request, not utf-8", e)
            conn.close()
            return

        # Extract host and path
        hostname = http_util.get_http_field(str_req, 'Host: ', const.END_LINE)
        pathname = http_util.get_http_field(str_req, 'GET ', ' HTTP/1.1')
        if hostname == -1 or pathname == -1:
            print ("Cannot determine host")
            conn.close()
            return
        elif pathname[0] != '/':
            [hostname, pathname] = http_util.parse_url(pathname)
        str_req = http_util.create_http_req(hostname, pathname)

        # Open connection to host and send binary request
        url = hostname + pathname

        # Let's check if the intended URL is already in our cache
        # If it is, we will prepare a conditional get request and
        # we'll note quickly that we sent the conditional request
        # as opposed to a regular request
        sentCondit = False
        if url in self.cache.keys():
            prefix = "If-Modified-Since: "
            midfix = self.cache[url]['lastmod']
            suffix = "\r\n"
            condition = prefix + midfix + suffix
            missing = "Accept-charset"
            parts = str_req.split(missing)
            out = parts[0] + condition + missing + parts[1]
            str_req = out
            sentCondit = True

        bin_req = str_req.encode('utf-8')
        try:
            web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            web_sock.connect((hostname, 80))
            print ("Sending request to web server: ", str_req)
            web_sock.sendall(bin_req)
        except OSError as e:
            print ("Unable to open web socket: ", e)
            if web_sock:
                web_sock.close()
            conn.close()
            return

        # Wait for response from web server
        bin_reply = b''
        while True:
            more = web_sock.recv(4096)
            if not more:
                 break
            bin_reply += more

        # Let's check what the returned message is i.e. 200 OK or 304 Not Modified
        # If we sent the conditional request and we get 304, we can simply forward
        # our cached url data. We also want to keep track of whether we want to add
        # this URL to cache. If the data hasn't been modified, then there's no
        # reason to change the data we have stored
        bin_print = bin_reply.decode('utf-8')
        isOkay = bin_print.split("TTP/1.1 ")
        isOkay = isOkay[1][:16]
        addtocache = True
        if sentCondit and isOkay == "304 Not Modified":
            bin_reply = self.cache[url]['data']
            addtocache = False

        # This code is intended to find the last modified date; if there is none we'll
        # use the returned date in the place of the last modified
        modfind = bin_print.split("Last-Modified: ")
        if len(modfind) > 1:
            modstart = modfind[1]
            modend = modstart[:29]
        else:
            modfind = bin_print.split("Date: ")
            modstart = modfind[1]
            modend = modstart[:29]

        # Once we've found the corresponding date, we'll check whether or not we want
        # to add this URL to cache. If we do, we'll save the date and the data for
        # future inquiries.
        if addtocache:
            self.cache[url] = {}
            self.cache[url]['lastmod'] = modend
            self.cache[url]['data'] = bin_reply
        

        # Send web server response to client
        conn.sendall(bin_reply)
        print('Proxy received from server (showing 1st 300 bytes): ', bin_print[:300])
        print()

        # Close connection to client
        conn.close()

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
