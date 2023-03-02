Remote TicTacToe Instructions
===
Okay! This was my first Computer Networks assignment!

The server.py file opens a web socket on its local network with a specified port number. It then waits for the client.py file to connect to it.

The server will ask the client for how many dimensions they want to play with and randomly choose who should go first. Client.py prompts the player to make moves of their own choice while server.py makes its own randomized moves. The system then loops between each player until the game is over. It will print who won and the client will disconnect from the socket while the computer listens for any other client.py's who might connect.

In order to run this program, make sure that whoever is running the server has the server file and tictactoe file in the same folder, and have them navigate to that directory in terminal. Whoever is running the client has to have the client and tictactoe file in the same folder and should do the same.

If one device is functioning as both the server and the client, simply put all the files into the same folder and open two separate terminal windows.

The server needs to be run first, for which one should type:
>python3 server.py

The client can then be run using:
>python3 client.py

See below for screenshots of the expected outputs. I have tried and tested the programs; if it returns any errors, they should be server related, so simply run the code again and it should work. If it continues to fail, be sure to enter the individual code files and make sure they use the same port number.
<img width="1440" alt="tictactoe1" src="https://user-images.githubusercontent.com/124002750/222592983-2b3adc11-234c-460a-a45e-a1796ca6db2e.png">
<img width="1440" alt="tictactoe2" src="https://user-images.githubusercontent.com/124002750/222593006-99c55669-818d-4a2a-b5c5-76b63978719e.png">
