#  /^^     /\    ^^^/  --|--
# |       /  \     /     |
# |  __  |----|   /      |
#  \__/  |    |  /___  __|__
# A Gazi Rahman Original Production!! (You're welcome friend)
#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Computer Networks, Spring 2023
# Homework 1: Tic-tac-toe game

import random
import binascii
import random
import socket
import sys

# Took this stuff from offered code on Comp332 website
def sock_read(sock):
    bin_data = b''
    while True:
        bin_data += sock.recv(4096)
        try:
            bin_data.decode('utf-8').index('DONE')
            break
        except ValueError:
            pass

    return bin_data[:-4].decode('utf-8')

# Same here lol
def sock_write(sock, str_data):
    str_data = str_data + 'DONE'
    bin_data = str_data.encode('utf-8')
    sock.send(bin_data)

class Board():
    """
    TicTacToe game board

    This class creates and keeps track of the state of the TicTacToe board. 
        - Complete display
        - Check for a winner
    """

    # I just downloaded a new text editor so I'm feeling confident :D

    # Basics of setting up a tictactoe board, we want to know the dimension n
    # such that we can create a square board of n x n dimensions
    def __init__(self, n):
        self.n = n
        self.setUp()

    # setUp() creates a list of lists under the name self.table. We can navigate
    # the self.table variable using self.table[x][y] for some 0 <= x < n and the
    # same constraint for y
    def setUp(self):
        self.table = []
        for row in range(self.n):
            xvals = []
            for yvals in range(self.n):
                #Filling empty list with space chars for easy printability
                xvals.append(" ")
            self.table.append(xvals)

    # Helper function, returns 1 if the value at the indicated coords matches entry,
    # returns 0 if not
    def isMatch(self, xcoord, ycoord, entry):
        return int(self.table[xcoord][ycoord] == entry)

    # LOTS of helper functions incoming, basically to check different methods
    # of victory and track who exactly won and how. I split them up to make them
    # modularized, especially since the homework says nothing about cost

    # Checks each row for victory based on whether
    # the entire row has the same character
    def checkWinHoriz(self):
        # Iterate through each row
        for row in range(len(self.table)):
            # Keep track of x's and o's
            numo = 0
            numx = 0
            # Check each index for x's and o's, adjust accordingly
            for column in range(len(self.table[row])):
                numo += self.isMatch(row, column, 'O')
                numx += self.isMatch(row, column, 'X')
            # Return statement if there's a winner
            if numo == self.n:
                return 'O won by filling row ' + str(row) + '!'
            if numx == self.n:
                return 'X won by filling row ' + str(row) + '!'
        # If we reach this point, there's no winner so we're returning None
        return None

    # Checking for a vertical victory based on whether any column has
    # every index with the same value
    def checkWinVert(self):
        # Same strategy as before but we're iterating through each column
        # instead of each row
        for column in range(self.n):
            numo = 0
            numx = 0
            for row in range(self.n):
                numo += self.isMatch(row, column, 'O')
                numx += self.isMatch(row, column, 'X')
            if numo == self.n:
                return 'O won by filling column ' + str(column) + '!'
            if numx == self.n:
                return 'X won by filling column ' + str(row) + '!'
        return None

    # Checking for a diagonal victory moving down and right from [0][0] by 
    # iterating through the vals with both the row and column vals increasing 
    # to maintain diagonal motion
    def checkWinSE(self):
        row = 0
        column = 0
        numo = 0
        numx = 0
        while row < self.n:
            numo += self.isMatch(row, column, 'O')
            numx += self.isMatch(row, column, 'X')
            row += 1
            column += 1
        if numo == self.n:
            return 'O won diagonally!'
        if numx == self.n:
            return 'X won diagonally'
        return None

    # Checking for diagonal victory again, but this time from [n-1][0]
    # going up and to rhe right, adjusting to maintain that path
    def checkWinNE(self):
        row = self.n - 1
        column = 0
        numo = 0
        numx = 0
        while row > -1:
            numo += self.isMatch(row, column, 'O')
            numx += self.isMatch(row, column, 'X')
            row -= 1
            column += 1
        if numo == self.n:
            return 'O won diagonally!'
        if numx == self.n:
            return 'X won diagonally!'
        return None

    def checkDraw(self):
        occupied = 0
        for xind in range(self.n):
            for yind in range(self.n):
                occupied += (self.table[xind][yind] != ' ')
        if occupied == (self.n ** 2):
            return 'This has been a draw!'
        return False

    # Finally deciding the victor, this one returns the kind
    # of victory if someone won, and returns False if no one did
    def checkWin(self):
        if not (self.checkWinHoriz() or self.checkWinVert() or \
            self.checkWinSE() or self.checkWinNE() or self.checkDraw()):
            return False
        if self.checkWinHoriz() != None:
            return self.checkWinHoriz()
        elif self.checkWinVert() != None:
            return self.checkWinVert()
        elif self.checkWinSE() != None:
            return self.checkWinSE()
        elif self.checkWinNE() != None:
            return self.checkWinNE()
        elif self.checkDraw() != None:
            return self.checkDraw()

    # We need a means to display the game board, and me being me, it should be
    # somewhat pretty.
    def display(self):
        # We want to mark the start of the board
        for cell in range(self.n):
            print("=====", end="")
        print()
        # Let's print by each row
        for row in range(self.n):
            # For each row, iterate through each column to be thorough
            for column in range(self.n):
                # With each value (row,column), we'll open and close the cell with |
                print("| " + self.table[row][column] + " |", end="")
            # We'll mark the end of the row
            print()
            for cell in range(self.n):
                print("=====", end="")
            print()

    # Ignore this part. I'm just making my own game board to test whether or
    # Not my functions all work
    def makeTest(self):
        self.n = 7
        self.setUp()
        self.table[3] = ['X','X','X','X','X','X','X']
        self.table[0][6] = 'O'
        self.table[1][6] = 'O'
        self.table[2][6] = 'O'
        self.table[4][6] = 'O'
        self.table[5][6] = 'O'
        self.table[6][6] = 'O'

class TicTacToe():
    """
    TicTacToe game

    This class keeps track of the state a TicTacToe game, with methods to be
    called when the server moves, when the user moves, and so on. For the Server’s
    tic-tac-toe strategy, you may choose a random strategy, or you may choose to
    implement something more intelligent. For the user’s strategy you should query
    the user.
    """

    def __init__(self, n):
        self.n = n
        self.board = Board(n)

    # Asks for row and then column to figure out where to put an O for the player
    def askInput(self):
        xval = input("Please enter the row for your intended coordinates from 0-" \
            + str(self.n - 1) + ": ")
        xval = int(xval)
        while xval < 0 or xval >= self.n:
            print("Your row entry is out of bounds!")
            xval = input("Please enter the row for your intended coordinates from 0-" \
            + str(self.n - 1) + ": ")
            xval = int(xval)
        yval = input("Please enter the column for your intended coordinates from 0-" \
            + str(self.n - 1) + ": ")
        yval = int(yval)
        while yval < 0 or yval >= self.n:
            print("Your column entry is out of bounds!")
            yval = input("Please enter the column for your intended coordinates from 0-" \
            + str(self.n - 1) + ": ")
            yval = int(yval)
        return xval,yval 
    
    def isOpen(self, xval, yval):
        return self.board.table[xval][yval] == ' '

    def playerMove(self):
        x,y = self.askInput()
        while not self.isOpen(x,y):
            print("That position is taken!")
            x,y = self.askInput()
        self.board.table[x][y] = 'O'
        print("Player move:")
        self.display()
        return (x,y)

    def manualPlayer(self, move):
        x = move[0]
        y = move[1]
        self.board.table[x][y] = 'O'
        print("Player move:")
        self.display()
        return (x,y)

    def toTuple(self, move):
        xval = ""
        yval = ""
        comma = 0
        for i in range(len(move))[1:-1]:
            if move[i] == ',':
                comma = i
                break
            xval += move[i]
        for i in range(len(move))[comma+1:-1]:
            yval += move[i]
        xval = int(xval)
        yval = int(yval)
        return xval,yval


    def compChoices(self):
        xvals = []
        yvals = []
        for index in range(self.n):
            xvals.append(index)
            yvals.append(index)
        xy = []
        for xindex in xvals:
            for yindex in yvals:
                xy.append((xindex,yindex))
        return xy

    def compMove(self):
        coords = self.compChoices()
        move = random.choice(coords)
        while not self.isOpen(move[0],move[1]):
            coords.remove(move)
            move = random.choice(coords)
        x = move[0]
        y = move[1]
        self.board.table[x][y] = 'X'
        print("Computer move:")
        self.display()
        return (x,y)        

    def manualComp(self, move):
        x = move[0]
        y = move[1]
        self.board.table[x][y] = 'X'
        print("Computer move:")
        self.display()
        return (x,y)  

    # Copied over from my Server code
    def askDimensions(self):
        dimensions = input("How many rows/columns would you like to play with? ")
        dimensions = int(dimensions)
        while dimensions <= 1:
            print("That's preposterous! Please take me seriously... or else!")
            dimensions = input("How many rows/columns would you like to play with? ")
            dimensions = int(dimensions)
        self.n = dimensions
        self.board = Board(dimensions)

    def chooseFirst(self):
        # True means the player goes first, False means the computer goes first
        first = random.choice([True,False])
        if first == True:
            print("Alright, player. You will move first.")
            return True
        else:
            print("Yay! I will go first")
            return False

    def printIntro(self):
        print("==================")
        print("| TicTacToe Game |")
        print("==================\n")

    def printBreak(self):
        print("\n=================================================================")
        print("=================================================================\n")

    def display(self):
        self.board.display()

