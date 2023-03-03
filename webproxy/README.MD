Web Proxy Guide
===
Okay! This system of files creates a web socket for a proxy, which listens on its local network for a web client. The client ask the proxy for the HTTP info of a website, which the proxy will process, create the request for, send the request, and then forward the results to the client. Once the results are forwarded, the client will close its connection with the proxy, while the proxy will keep the web socket open, listening for more devices on its local network. This is a build up to my proxyandcache project also in this repository.

The client in this case automatically requests example.com. You can change this by manually going into the file and asking for a different URL. Note, though, that right now this code only works for HTTP requests, not HTTPS.

In order for this system of files to work on multiple devices, they must all be connected to the same devices.

To run this system of files, run the proxy in one terminal window by typing:
>python3 web_proxy.py

Afterwards, run the client in either the terminal of another device or another terminal window on the same device by typing:
>python3 web_client.py

The results should look like the screenshot below. You'll notice that the proxy prints the request it created for the client, and the client prints the HTML info of the website it asked for. If the code does not work, ensure that your URL is HTTP and not HTTPS. If it still does not work, ensure that the proxy and client code both have the same port numer.
<img width="1440" alt="proxy" src="https://user-images.githubusercontent.com/124002750/222594440-368a0f8c-cf82-4646-a65f-7a83580add08.png">
