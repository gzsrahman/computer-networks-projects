Proxy and Cache Guide
===
Okay! This jumps off of my previous webproxy code. See the README file in that repository for context.

Essentially, the system of files is comprised of web_proxy.py and web_client.py. In order for the system to work over multiple devices, they must all be run on the same network. You may also run the code on the same device using two different terminal windows.

On one device, run the following first:
>python3 web_proxy.py

On another device or a different terminal window on the same device, run:
>python3 web_client.py

The web proxy opens up a socket on the local network, waiting for the web client to connect. The client will request the HTTP info of a URL specified inside the file; you are welcome to change the URL so long as it is on HTTP. The client asks the proxy for the HTTP info of said URL.

The difference between this project and the aforementioned one is that this proxy implements the use of a cache. When the client requests the HTTP info of a website that hasn't been requested yet, just like before, the proxy will create a request, send it to the web server, and receive the returned info. This time though, before the proxy sends the HTTP info to the client, it will store the url and under it information about when the website was last modified as well as the return. If it doesn't know when the website was last modified, it will simply store the current date. Afterwards, the proxy will finally forward the HTTP info to the client. The client will disconnect and the proxy will keep listening.

However, during this runtime while the proxy is still listening, when a client requests the HTTP info of a pre-requested URL, the proxy will check its cache. It will create a conditional HTTP request, essentially saying, "Please only give me the HTTP info if it has been modified since I last requested." If the info has been modified, then the server will give the proxy the new information. The proxy will update its info before forwarding it to the client. However, if the info wasn't modified, then the proxy will simply forward the information that it already stored in its cache.

See the screenshots below of the proxy and client running in terminal. The proxy also works with your browser when you visit HTTP websites! Simply set up a local proxy specified to the name local host. Set the port number to what is listed at the bottom of web_proxy.py. Screenshots of this are also included below.
<img width="1440" alt="part1" src="https://user-images.githubusercontent.com/124002750/222602550-e129dbcf-44ae-4d23-9a23-4f5ba2145a38.png">
<img width="1440" alt="part2" src="https://user-images.githubusercontent.com/124002750/222602562-9a5741a3-a82b-4280-859b-7cfebd215af0.png">
