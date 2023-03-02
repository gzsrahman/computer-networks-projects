# ###########################################################
#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)

Okay this project requires the use of:
    http_constants.py
    http_util.py
    web_client.py
    web_proxy.py
I know I know. "Ohhhhhhh he's such a loser he's using the given code instead
of his own!!" Listen... Bears can run faster than speeds of 25mph.

You're gonna want all these files to be in the same directory so that my web*
files can call upon my http* files. Basically just run:
    python3 web_proxy.py
And then uncomment your choice of url in web_client.py and run:
    python3 web_client.py
Make sure the port numbers are the same!! I've kept them the same for
submission but I dunno, maybe it is worth mentioning. Be kind while grading.
If you want to use the proxy in your browser, set up a local proxy in your
device citing the host as localhost and the port as the port number listed
in web_proxy.py. Run the web proxy as instructed above and then go to any
http website in your browser. You should see a return under your terminal
window that's running web_proxy.py