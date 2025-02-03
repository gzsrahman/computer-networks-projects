Chat App Guide
===
This folder contains a mini-chat system I created that runs over terminal! For right now, this adaptation only works running the server and client on the same device.

To begin, run the server in one terminal window by navigating to the appropriate directory and entering:
> python3 chat_server.py
Afterwards, you may create as many clients as you like by opening new terminal windows and entering:
> python3 chat_client.py

The chat server opens a TCP socket and listens for client connections. 

When the chat client is run, it connects to the server and asks the user for their name; the client then sends the name to the server. The server keeps a dictionary of each client connection, their network address, and the name they entered. When new clients enter the server, their entry and name are communicated to every existing client.

When clients send messages to the server, the server prints a log of everything that is sent and from whom. When the server forwards the message to other clients, since it keeps track of the name, other clients are given the name of the sender as well as the message. In addition, when a client leaves, which they can do by pressing CTRL + C, all the other clients are notified of who exactly left.

Even when all the clients leave, the server will listen for new connections and retain its log of the conversation.

See below for screenshots of the system in action:
![Screenshot 2023-04-12 at 9 15 48 PM](https://user-images.githubusercontent.com/124002750/231620758-18150a6b-5fd4-4ddd-b43b-277deef8c7d2.jpg)
![Screenshot 2023-04-12 at 9 16 01 PM](https://user-images.githubusercontent.com/124002750/231620769-ef25d559-e982-492e-8f59-ac91b9ec665f.jpg)
![Screenshot 2023-04-12 at 9 16 19 PM](https://user-images.githubusercontent.com/124002750/231620780-6159041f-7762-488a-bf56-1b4daed1dc00.jpg)
![Screenshot 2023-04-12 at 9 16 35 PM](https://user-images.githubusercontent.com/124002750/231620787-6a7e4de1-32ef-414f-86fb-098ac2b75f89.jpg)
![Screenshot 2023-04-12 at 9 16 58 PM](https://user-images.githubusercontent.com/124002750/231620794-d9aec760-6df5-4adb-a1ed-31c9b4ba56df.jpg)
![Screenshot 2023-04-12 at 9 17 13 PM](https://user-images.githubusercontent.com/124002750/231620799-54e55c69-14cb-4c70-9742-9e0fc32ed592.jpg)
![Screenshot 2023-04-12 at 9 17 28 PM](https://user-images.githubusercontent.com/124002750/231620807-fb9e0687-638d-411f-a2d8-405fb1f4253e.jpg)
![Screenshot 2023-04-12 at 9 18 04 PM](https://user-images.githubusercontent.com/124002750/231620816-f87379e0-2f23-4271-8e3e-14995f22f8bc.jpg)
![Screenshot 2023-04-12 at 9 18 16 PM](https://user-images.githubusercontent.com/124002750/231620828-bf1d0899-ee7d-4064-94f9-36051809fd13.jpg)
