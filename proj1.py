#File: proj1.py
#Name: Sam Routt
#Date: 4/5/16
#Section: 20
#Email: sroutt1@umbc.edu
#Description: plays tic-tac-toe between 2 human players

import random

DEFAULT_BOARD = '''
- - - - - - - 
| 1 | 2 | 3 |
- - - - - - -
| 4 | 5 | 6 |
- - - - - - -
| 7 | 8 | 9 |
- - - - - - -
'''
ACTIVE_POSITIONS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
WINNING_POSITIONS = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))

#Input: board, player, current symbol, current positions
#Output: if the user wants to play again or not
#Description: saves data from the current game into a basic string format separated by ";"
def saveGame(board, player, symbol, positions):
    myFile = open('tic.txt', 'w')
    posString = ''
    for i in positions:
        posString += i
    bigString = board + ';' + str(player) + ';' + symbol + ';' + posString
    myFile.write(bigString)
    myFile.close()
    playAgain = ''
    #Gets a valid choice for playAgain
    while playAgain != 'yes' and playAgain != 'no':
        playAgain = input('Play again? (yes or no): ')
        if playAgain != 'yes' and playAgain != 'no':
            print('Invalid answer. Please enter "yes" or "no"')
        if playAgain == 'no':
            print('Thanks for playing!')
    return playAgain

#Input: n/a
#Output: board, player, symbol, positions from previous game
#Description: splits savefile up and converts data into appropriate data types and variables
def loadGame():
    myFile = open('tic.txt', 'r')
    bigString = myFile.read()
    board, player, symbol, posString = bigString.split(';')
    positions = [None] * len(posString)
    #Changes positions from string to list
    for i in range(0, len(posString)):
        positions[i] = posString[i]
    #Assigns player value
    if player == '1':
        player = 1
    else:
        player = 2    
    myFile.close()
    return board, player, symbol, positions

#Input: board, getChoice(), symbol
#Output: modified board
#Description: splits board on "choice" and replaces it with the current symbol.
def getBoard(board, choice, symbol):
    halfBoard = board.split(choice)
    newBoard = halfBoard[0] + symbol + halfBoard[1]
    return newBoard

#Input: current positions, player, and symbol
#Output: valid choice from user
#Description: gets user choice of vacant positions and returns integer choice
def getChoice(positions, player, symbol):
    print('\nPlayer', str(player), 'what is your choice?')
    choice = 0
    #Loops until a valid choice is given by the user
    while choice < -2 or choice == 0 or choice > 9:
        choice = int(input('(1-9) or -1 to save or -2 to load: '))
        #Checks to see if choice is occupied
        if choice > 0 and choice < 10:
            while positions[choice - 1] == 'X' or positions[choice - 1] == 'O':
                if positions[choice - 1] == 'X' or positions[choice - 1] == 'O':
                    print('That space is already being used. Enter a new choice.')
                    choice = int(input('(1-9) or -1 to save or -2 to load: '))
        elif choice < -2 or choice == 0 or choice > 9:
            print('That is not a valid choice. Enter a new choice.')
    return choice

#Input: current player and symbol
#Output: next turn's player and symbol
#Description: changes the value of player and symbol after each turn
def nextTurn(player, symbol):
    if symbol == 'X':
        symbol = 'O'
    else:
        symbol = 'X'
    
    if player == 1:
        player = 2
    else:
        player = 1
    return player, symbol

#Input: player, symbol, positons
#Output: if the game is won or not, and user response for playAgain
#Description: returns true if game is won; false otherwise, and asks if user wants to play again
def gameOver(player, symbol, positions):
    isWon = False
    playAgain = ''
    #Checks all posibilities of win conditions
    for i in range(0, len(WINNING_POSITIONS)):
        counter = 0
        #counts consecutive symbols in winning lines and determines value for isWon and playAgain
        for x in WINNING_POSITIONS[i]:
            if positions[x - 1] == symbol:
                counter += 1
            if counter == 3:
                isWon = True
                print('Player', str(player), 'wins!')
                while playAgain != 'yes' and playAgain != 'no':
                    playAgain = input('Play again? (yes or no): ')
                    if playAgain != 'yes' and playAgain != 'no':
                        print('Invalid answer. Please enter "yes" or "no"')
                    if playAgain == 'no':
                        print('Thanks for playing!')
    return isWon, playAgain
        
def main():
    print('\nWelcome to Tic-Tac-Toe!')
    print('This is for two players.')
    player = ''
    symbol = ''
    positions = [None] * 9
    playAgain = 'yes'
    #Loops for every consecutive game within the same runtime
    while playAgain == 'yes':
        #Gets random values for player and symbol
        player = random.randint(1, 2)
        symbolNum = random.randint(1, 2)
        symbol = ''
        if symbolNum == 1:
            symbol = 'X'
        else:
            symbol = 'O'
        print('Player', str(player), 'will go first and will play with', symbol)
        board = DEFAULT_BOARD
        #Assigns values for positions
        for i in range(len(positions)):
            positions[i] = str(i + 1)
        print(DEFAULT_BOARD)
        choice = 0
        isWon = False
        #Loops until game is won or game is saved
        while isWon == False and choice != '-1':
            choiceInt = getChoice(positions, player, symbol)
            choice = str(choiceInt)
            #saves game
            if choice == '-1':
                print('Game saved.')
                playAgain = saveGame(board, player, symbol, positions)
            #Loads game
            elif choice == '-2':
                print('Game loaded.')
                board, player, symbol, positions = loadGame()
                print(board)
            #Passes choice to getBoard() and changes turn
            else:
                positions[choiceInt - 1] = symbol
                board = getBoard(board, choice, symbol)
                print(board)
                isWon, playAgain = gameOver(player, symbol, positions)
                player, symbol = nextTurn(player, symbol)
    print()
main()
