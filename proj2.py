#File: proj2.py
#Name: Sam Routt
#Date: 5/7/16
#Section: 20
#Email: sroutt1@umbc.edu
#Description: Prints the starting location and direction of words in a word search.

DIRECTIONS = ((-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1))
DIR_STRINGS = ('diagonally up and left','up','diagonally up and right','right','diagonally down and right','down','diagonally down and left','left')

#Input: puzzle file path
#Output: 2d puzzle list
#Description: gets a big-string word-search from a .txt and converts it to a 2d list
def setPuzzle(puzzleFile):
    myFile = open(puzzleFile)
    puzzleLines = myFile.readlines()
    puzzle = []
    #splits file string into single character elements and puts them in a 2d list
    for i in range(len(puzzleLines)):
        letters = puzzleLines[i].split(' ')
        letters[len(letters)-1] = letters[len(letters)-1][0:1]
        puzzle.append(letters)
    myFile.close()
    return puzzle

#Input: word list file path
#Output: wordList
#Description: converts word list string into a list and cuts off '\n' from each word.
def setWordList(wordListFile):
    myFile = open(wordListFile)
    tempList = myFile.readlines()
    wordList = []
    #puts lines from myFile into a list
    for i in tempList:
        word = i[0:len(i)-1] 
        wordList.append(word)
    return wordList

#Input: DIRECTIONS index
#Output: string representation of direction
#Description: returns string of direction to be printed later
def getDirString(index):
    dirString = DIR_STRINGS[index]
    return dirString
    
#Input: startPosition, word, newWord, puzzle, currentPos, counter, direction
#Output: direction of word in word search
#Description: Uses recursion to check all directions around startPosition. returns direction
def checkDir(startPosition, word, newWord, puzzle, currentPos, counter, direction):
    row = currentPos[0]
    col = currentPos[1]
    #Terminates if all directions have been searched
    if counter < len(DIRECTIONS):
        newRow = row + DIRECTIONS[counter][0]
        newCol = col + DIRECTIONS[counter][1]
        #Changes row if all columns have been checked. proceeds otherwise
        if newRow >= 0 and newCol >= 0 and newRow < len(puzzle) and newCol < len(puzzle[0]) and len(newWord) < len(word):
            newWord += puzzle[newRow][newCol]
            currentPos = [newRow, newCol]
            #Determines if direction contains word being searched
            if newWord == word:
                direction = getDirString(counter)
                return checkDir(startPosition, word, newWord, puzzle, currentPos, counter, direction)
            else:
                return checkDir(startPosition, word, newWord, puzzle, currentPos, counter, direction)
        else:
            counter += 1
            return checkDir(startPosition, word, word[0], puzzle, startPosition, counter, direction)
    return direction

#Input: word, puzzle, row, col, startPositions
#Output: startPositions list
#Description: appends positions of first letter in word to a list and returns it.
def findStartPos(word, puzzle, row, col, startPositions):
    firstLetter = word[0]
    #Terminates if each element in puzzle has been searched.
    if row < len(puzzle):
        #Checks all columns in row and finds pos of letters that match firstLetter of word.
        if col < len(puzzle[0]):
            #Compares element in puzzle to first letter of word
            if puzzle[row][col] == firstLetter:
                startPositions.append([row, col])
            col += 1
        else:
            row += 1
            col = 0
        findStartPos(word, puzzle, row, col, startPositions)
    return startPositions
 
#Input: wordList, puzzle
#Output: N/A
#Description: prints if word is in puzzle and the startPosition and direction of each word.
def findWords(wordList, puzzle):
    #passes words through search functions.
    for i in wordList:
        counter = 0
        startPositions = findStartPos(i, puzzle, 0, 0, [])
        direction = ''
        #Ends when word is found and assigns correct values to pos and direction of word
        while direction == '' and counter < len(startPositions):
            pos = startPositions[counter]
            row = str(pos[0])
            col = str(pos[1])
            counter += 1
            direction = checkDir(pos, i, i[0], puzzle, pos, 0, '')
        #Prints information about word
        if direction != '':
            print('The word', i, 'starts in (' + row + ',', col + ') and goes', direction)
        else:
            print('The word', i, 'does not appear in the puzzle.')

#Input: N/A
#Output: 2d puzzle list and word list
#Description: gets filenames for wordList and puzzle. passes to main().
def intro():
    print('Welcome to the Word Search.')
    print('For this, you will import two files: 1. The puzzle board, and 2. The word list.')
    puzzle = input('What is the puzzle file you would like to import? ')
    wordList = input('What is the word list file you would like to import? ')
    return puzzle, wordList

def main():
    puzzleFile, wordListFile = intro()
    puzzle = setPuzzle(puzzleFile)
    wordList = setWordList(wordListFile)
    findWords(wordList, puzzle)

main()
