import sys
import random


class Game:

    # Constructor
    def __init__(self):
        self.boardSize = 8

        # The current state represents the board : 0=no player,  1=player1, 2=player2
        self.getNewBoard()

        # Player black always plays first
        self.currentPlayer = 'B'

    # Creates a new board
    def getNewBoard(self):
        # Creates a brand new, blank board data structure.
        self.current_state = []
        for i in range(self.boardSize):
            self.current_state.append(['.'] * self.boardSize)
        self.current_state[self.boardSize//2 - 1][self.boardSize//2-1] = 'W'
        self.current_state[self.boardSize//2 - 1][self.boardSize//2] = 'B'
        self.current_state[self.boardSize//2][self.boardSize//2-1] = 'B'
        self.current_state[self.boardSize//2][self.boardSize//2] = 'W'

    # Returns True if the coordinates are located on the board.
    def isOnBoard(self, x, y):
        return x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize

    # Determines if the made move is a legal move
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    def isValidMove(self, coin, line, column):
        if not self.isOnBoard(line, column):
            return False
        elif self.current_state[line][column] != '.':
            return False
        else:
            opponentCoin = self.getOppositePlayer(coin)
            allCoinsToFlip = []  # The posotion of all tiles to move
            for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                x, y = line, column
                x += xdirection
                y += ydirection
                newCoinsToFlip = []
                # Look for all coins in the current direction, who are of the opposite color from the one played, until it reaches a coin of an other collor or the end of the board
                while self.isOnBoard(x, y) and self.current_state[x][y] == opponentCoin:
                    newCoinsToFlip.append([x, y])
                    x += xdirection
                    y += ydirection
                # If the last coin in this direction is of the same color as the coin played, all the coins inside newCoinsToFlip are to be flipped
                if self.isOnBoard(x, y) and self.current_state[x][y] == coin:
                    allCoinsToFlip += newCoinsToFlip

            # If no tiles were flipped, this is not a valid move
            if len(allCoinsToFlip) == 0:
                return False

            return allCoinsToFlip

    # Try to play a move
    # Return bolean saying whether the move could be made and if so update the current state
    def play_move(self, currentPlayer, line, column):
        allCoinsToFlip = self.isValidMove(currentPlayer, line, column)

        # If it is not valid don't perform the move
        if allCoinsToFlip == False:
            return False
        # Otherwise flip all coins
        else:
            self.current_state[line][column] = currentPlayer
            for posX, posY in allCoinsToFlip:
                self.current_state[posX][posY] = currentPlayer
            return True

    # Play a move: flip all coins specified in allCoinsToFlip
    # Precondition: the move must be valid and the list correct
    def playMoveWithListOfAllCoinsToFlip(self, currentPlayer, line, column, allCoinsToFlip):
        self.current_state[line][column] = currentPlayer
        for posX, posY in allCoinsToFlip:
            self.current_state[posX][posY] = currentPlayer

    # Undo a played move: flip back all coins specified in allCoinsToFlip and remove the added coin
    # Precondition: the move must be valid and the list correct
    def undoPlayedMoveWithListOfAllCoinsToFlip(self, currentPlayer, line, column, allCoinsToFlip):
        self.current_state[line][column] = "."
        oppositePlayer = self.getOppositePlayer(currentPlayer)
        for posX, posY in allCoinsToFlip:
            self.current_state[posX][posY] = oppositePlayer
        return True

    # Returns a dictionary of {["line,column"] = [line, column, allCoinsToFlip]} lists of valid moves for the given player on the given board and the asociated coins to flip.
    def getValidMoves(self, currentPlayer):
        validMoves = {}
        for line in range(self.boardSize):
            for column in range(self.boardSize):
                allCoinsToFlip = self.isValidMove(currentPlayer, line, column)
                if allCoinsToFlip != False:
                    key = str(line)+","+str(column)
                    validMoves[key] = [line, column, allCoinsToFlip]
        return validMoves

    # Return the color of the opposite player of the current player
    def getOppositePlayer(self, currentPlayer):
        if currentPlayer == 'W':
            return 'B'
        else:
            return 'W'

    # Method to play the game
    def play(self):
        runGame = True
        while runGame:
            # Initialize the game by asking the player whether they want to play against a computer
            playerBlackType = self.askPlayerType("Black")
            if playerBlackType == 2:
                self.playerBlackHeuristic = self.askWantedHeuristic("Black")
                # Ask the search depth for the minimax algorithm if the heuristic is not random
                if self.playerBlackHeuristic != 1:
                    playerBlackMaxSearchDepth = self.askWantedSearchDepth(
                        "Black")
            playerWhiteType = self.askPlayerType("White")
            if playerWhiteType == 2:
                self.playerWhiteHeuristic = self.askWantedHeuristic("White")
                # Ask the search depth for the minimax algorithm if the heuristic is not random
                if self.playerWhiteHeuristic != 1:
                    playerWhiteMaxSearchDepth = self.askWantedSearchDepth(
                        "White")

            gameOver = False
            previousCouldPlay = True
            self.getNewBoard()
            self.draw_board()

            while not gameOver:
                # Store all valid moves and the associated list of coins to flip
                allValidMoves = self.getValidMoves(self.currentPlayer)
                if len(allValidMoves) != 0:
                    print("Player " + self.currentPlayer + "'s turn")
                    # Black player's turn
                    if self.currentPlayer == 'B':
                        # If the player is human ask the position where the player wants to play
                        if playerBlackType == 1:
                            (line, column, allCoinsToFlip) = self.askPlayerMoveWithMapOfValidMoves(
                                self.currentPlayer, allValidMoves)
                        # If the player chooses the nect moove randomly
                        elif self.playerBlackHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.max(
                                0, playerBlackMaxSearchDepth, -sys.maxsize, sys.maxsize)
                    # White player's turn
                    else:
                        # If the player is human ask the position where the player wants to play
                        if playerWhiteType == 1:
                            (line, column, allCoinsToFlip) = self.askPlayerMoveWithMapOfValidMoves(
                                self.currentPlayer, allValidMoves)
                        # If the player chooses the nect moove randomly
                        elif self.playerWhiteHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.min(
                                0, playerWhiteMaxSearchDepth, -sys.maxsize, sys.maxsize)

                    # Play the move by updating the board
                    self.playMoveWithListOfAllCoinsToFlip(
                        self.currentPlayer, line, column, allCoinsToFlip)
                    self.draw_board()
                    self.currentPlayer = self.getOppositePlayer(
                        self.currentPlayer)
                    previousCouldPlay = True

                # If the current palyer can not play, the plyer skip his turn
                else:
                    if (previousCouldPlay):
                        self.currentPlayer = self.getOppositePlayer(
                            self.currentPlayer)
                        previousCouldPlay = False
                    # If the prvious and the current player can not play, then the game is over
                    else:
                        gameOver = True
            # End of the game
            nbBlack, nbWhite = self.getScore()
            print("Player Black has " + str(nbBlack) +
                  " coins and player White has " + str(nbWhite) + " coins.")
            if nbBlack > nbWhite:
                print("Player Black wins!")
            elif nbBlack < nbWhite:
                print("Player White wins!")
            else:
                print("It's a tie!")

            # Ask the player if they want to play again
            print()
            playAgain = self.askPlayAgain()
            print()
            if playAgain == 2:
                runGame = False
        print("Bye! Thank you for playing.")

    # Method to play the game automaticaly
    def autoPlay(self, nbGames, playerBlackHeuristic, playerBlackMaxSearchDepth, playerWhiteHeuristic, playerWhiteMaxSearchDepth):

        nbWinBlack = 0
        nbWinWhite = 0
        nbDraw = 0

        for i in range(nbGames):
            # Initialize the game by asking the player whether they want to play against a computer
            self.playerBlackHeuristic = playerBlackHeuristic
            self.playerWhiteHeuristic = playerWhiteHeuristic

            gameOver = False
            previousCouldPlay = True
            self.getNewBoard()

            while not gameOver:
                # Store all valid moves and the associated list of coins to flip
                allValidMoves = self.getValidMoves(self.currentPlayer)
                if len(allValidMoves) != 0:
                    # Black player's turn
                    if self.currentPlayer == 'B':
                        # If the player chooses the next moove randomly
                        if self.playerBlackHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.max(
                                0, playerBlackMaxSearchDepth, -sys.maxsize, sys.maxsize)
                    # White player's turn
                    else:
                        # If the player chooses the nect moove randomly
                        if self.playerWhiteHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.min(
                                0, playerWhiteMaxSearchDepth, -sys.maxsize, sys.maxsize)

                    # Play the move by updating the board
                    self.playMoveWithListOfAllCoinsToFlip(
                        self.currentPlayer, line, column, allCoinsToFlip)

                    self.currentPlayer = self.getOppositePlayer(
                        self.currentPlayer)
                    previousCouldPlay = True

                # If the current palyer can not play, the plyer skip his turn
                else:
                    if (previousCouldPlay):
                        self.currentPlayer = self.getOppositePlayer(
                            self.currentPlayer)
                        previousCouldPlay = False
                    # If the prvious and the current player can not play, then the game is over
                    else:
                        gameOver = True
            # End of the game
            nbBlack, nbWhite = self.getScore()
            if nbBlack > nbWhite:
                nbWinBlack += 1
            elif nbBlack < nbWhite:
                nbWinWhite += 1
            else:
                nbDraw += 1
            print("For " + str(i+1) + " games: player Black won " + str(nbWinBlack) +
                  " times, payer White won " + str(nbWinWhite) + " times and there were " + str(nbDraw) + " draws.")

    # Method to play the game automaticaly in parallel
    def autoPlayParallel(self, playerBlackHeuristic, playerBlackMaxSearchDepth, playerWhiteHeuristic, playerWhiteMaxSearchDepth):
        # Initialize the game by asking the player whether they want to play against a computer
        self.playerBlackHeuristic = playerBlackHeuristic
        self.playerWhiteHeuristic = playerWhiteHeuristic

        gameOver = False
        previousCouldPlay = True
        self.getNewBoard()

        while not gameOver:
            # Store all valid moves and the associated list of coins to flip
            allValidMoves = self.getValidMoves(self.currentPlayer)
            if len(allValidMoves) != 0:
                # Black player's turn
                if self.currentPlayer == 'B':
                    # If the player chooses the next moove randomly
                    if self.playerBlackHeuristic == 1:
                        (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                            allValidMoves)
                    # If the player is an AI, computes the next move
                    else:
                        (value, line, column, allCoinsToFlip) = self.max(
                            0, playerBlackMaxSearchDepth, -sys.maxsize, sys.maxsize)
                # White player's turn
                else:
                    # If the player chooses the nect moove randomly
                    if self.playerWhiteHeuristic == 1:
                        (line, column, allCoinsToFlip) = self.chooseRandomMoveWithMapOfValidMoves(
                            allValidMoves)
                    # If the player is an AI, computes the next move
                    else:
                        (value, line, column, allCoinsToFlip) = self.min(
                            0, playerWhiteMaxSearchDepth, -sys.maxsize, sys.maxsize)

                # Play the move by updating the board
                self.playMoveWithListOfAllCoinsToFlip(
                    self.currentPlayer, line, column, allCoinsToFlip)

                self.currentPlayer = self.getOppositePlayer(
                    self.currentPlayer)
                previousCouldPlay = True

            # If the current palyer can not play, the plyer skip his turn
            else:
                if (previousCouldPlay):
                    self.currentPlayer = self.getOppositePlayer(
                        self.currentPlayer)
                    previousCouldPlay = False
                # If the prvious and the current player can not play, then the game is over
                else:
                    gameOver = True
        # End of the game
        nbBlack, nbWhite = self.getScore()
        if nbBlack > nbWhite:
            return 'B'
        elif nbBlack < nbWhite:
            return 'W'
        else:
            return 'D'

    # Return the nb of coins for the bleck and white player
    def getScore(self):
        nbBlack = 0
        nbWhite = 0
        for line in range(self.boardSize):
            for column in range(self.boardSize):
                if self.current_state[line][column] == 'B':
                    nbBlack += 1
                elif self.current_state[line][column] == 'W':
                    nbWhite += 1
        return nbBlack, nbWhite

    # Pick a move randomly
    # Precondition: the list must contain only valid moves
    # Return the chosen move
    def chooseRandomMoveWithMapOfValidMoves(self, allValidMoves):
        move = list(allValidMoves.values())
        choice = random.choice(move)
        return choice[0], choice[1], choice[2]

    # Max function of the minimax algorithm. The Black player seeks the maximum value whereas the White player seeks the minimum value
    # Stop the recursive search when the current state is a leaf or the maximum search depyh was reached. It also uses the alpha beta pruning to stop searching in useless branches.
    # Return the maximum value of all child nodes and the position to play to get to this child node and the associated list of coins to flip.
    def max(self, currDepth, maxSearchDepth, alpha, beta):
        # Compute the next states
        # Store all valid moves that can be played from the currend state and the associated list of coins to flip
        allValidMoves = self.getValidMoves('B')

        # If there is no next states or it reached the maxSearchDepth, the function needs to return the evaluation function of the end.
        if currDepth >= maxSearchDepth or len(allValidMoves) == 0:
            return (self.evaluateState(), 0, 0, [])

        currDepth += 1

        maxValue = -sys.maxsize - 1  # The wost posssible value
        maxLine = None
        maxColumn = None
        maxValueAllCoinsToFlip = []
        storeMaxValueData = []

        # Play all following moves. Search the child node with the maximum value
        for key, move in allValidMoves.items():
            # Play the move by updating the board
            self.playMoveWithListOfAllCoinsToFlip(
                'B', move[0], move[1], move[2])
            # Search the min value of the child node of this node
            (minValueChildNode, minChildLine, minChildColumn, minChildAllCoinsToFlip) = self.min(
                currDepth, maxSearchDepth, alpha, beta)

            # Undo the move to get back to the current state
            self.undoPlayedMoveWithListOfAllCoinsToFlip(
                'B', move[0], move[1], move[2])

            # Find the child node with the maximum value
            if minValueChildNode >= maxValue:
                # If the value is greater than the current max, create a new max list
                if minValueChildNode > maxValue:
                    storeMaxValueData.clear()
                maxValue = minValueChildNode
                maxLine = move[0]
                maxColumn = move[1]
                maxValueAllCoinsToFlip = move[2]
                storeMaxValueData.append(
                    [maxLine, maxColumn, maxValueAllCoinsToFlip])

            # Pruning whith the alpha beta method
            # If the maxValue is greater than the current best value of the min player(beta) then min player is never going to play the currrent node. Hence it is useless to continue to explore the child of this node
            if maxValue > beta:
                return (maxValue, maxLine, maxColumn, maxValueAllCoinsToFlip)

            # Update the alpha value : the current best value of the max player
            if maxValue > alpha:
                alpha = maxValue

        # If 2 or more child nodes return the same value after evaluation, randomly pick one of them
        if len(storeMaxValueData) > 0:
            choice = random.choice(storeMaxValueData)
            maxLine = choice[0]
            maxColumn = choice[1]
            maxValueAllCoinsToFlip = choice[2]

        # Return the maximum value of the child node and the position to play to get to this child node.
        return (maxValue, maxLine, maxColumn, maxValueAllCoinsToFlip)

    # Min function of the minimax algorithm. The Black player seeks the maximum value whereas the White player seeks the minimum value
    # Stop the recursive search when the current state is a leaf or the maximum search depyh was reached. It also uses the alpha beta pruning to stop searching in useless branches.
    # Return the minimum value of all child nodes and the position to play to get to this child node and the associated list of coins to flip.
    def min(self, currDepth, maxSearchDepth, alpha, beta):
        # Compute the next states
        # Store all valid moves and the associated list of coins to flip
        allValidMoves = self.getValidMoves('W')

        # If there is no next states or it reached the maxSearchDepth, the function needs to return the evaluation function of the end.
        if currDepth >= maxSearchDepth or len(allValidMoves) == 0:
            return self.evaluateState(), 0, 0, []

        currDepth += 1

        minValue = sys.maxsize  # The best posssible value
        minLine = None
        minColumn = None
        minValueAllCoinsToFlip = []
        storeMinValueData = []

        # Play all following moves. Search the child node with the minimum value
        for key, move in allValidMoves.items():
            # Play the move by updating the board
            self.playMoveWithListOfAllCoinsToFlip(
                'W', move[0], move[1], move[2])
            # Search the max value of the child node of this node
            (maxValueChildNode, maxChildLine, maxChildColumn, maxChildAllCoinsToFlip) = self.max(
                currDepth, maxSearchDepth, alpha, beta)

            # Undo the move to get back to the current state
            self.undoPlayedMoveWithListOfAllCoinsToFlip(
                'W', move[0], move[1], move[2])

            # Find the child node with the minimum value
            if maxValueChildNode <= minValue:
                # If the value is less than the current min, create a new min list
                if maxValueChildNode < minValue:
                    storeMinValueData.clear()
                minValue = maxValueChildNode
                minLine = move[0]
                minColumn = move[1]
                minValueAllCoinsToFlip = move[2]
                storeMinValueData.append(
                    [minLine, minColumn, minValueAllCoinsToFlip])

            # Pruning whith the alpha beta method
            # If the minValue is smaller than the current best value of the max player (alpha) then max player is never going to play the currrent node. Hence it is useless to continue to explore the child of this node
            if minValue < alpha:
                return minValue, minLine, minColumn, minValueAllCoinsToFlip

            # Update the beta value : the current best value of the min player
            if minValue < beta:
                beta = minValue

        # If 2 or more child nodes return the same value after evaluation, randomly pick one of them
        if len(storeMinValueData) > 0:
            choice = random.choice(storeMinValueData)
            minLine = choice[0]
            minColumn = choice[1]
            minValueAllCoinsToFlip = choice[2]

        # Return the maximum value of the child node and the position to play to get to this child node.
        return minValue, minLine, minColumn, minValueAllCoinsToFlip

    # This function evaluates the current state whith the evaluation function of the currentPlayer
    # Return the value of the evaluation wich belongs to this intervall [-100, 100]
    def evaluateState(self):
        if self.currentPlayer == "B":
            evalFunctionNumber = self.playerBlackHeuristic
        else:
            evalFunctionNumber = self.playerWhiteHeuristic

        if evalFunctionNumber == 2:
            value = self.evaluationStatic()
        elif evalFunctionNumber == 3:
            value = self.evaluationCornersCaptured()
        else:
            value = 0
        return value

    # Return the evaluation of the current state according the static method
    def evaluationStatic(self):
        staticWeights = [[50,  -3,  2,  2,  2,  2, -3, 50],
                         [-3, -4, -1, -1, -1, -1, -4, -3],
                         [2,  -1,  1,  0,  0,  1, -1,  2],
                         [2,  -1,  0,  1,  1,  0, -1,  2],
                         [2,  -1,  0,  1,  1,  0, -1,  2],
                         [2,  -1,  1,  0,  0,  1, -1,  2],
                         [-3, -4, -1, -1, -1, -1, -4, -3],
                         [50,  -3,  2,  2,  2,  2, -3,  50]]
        costBlack = 0
        costWhite = 0
        for line in range(self.boardSize):
            for column in range(self.boardSize):
                if self.current_state[line][column] == 'B':
                    costBlack += staticWeights[line][column]
                elif self.current_state[line][column] == 'W':
                    costWhite += staticWeights[line][column]
        return costBlack - costWhite

    # Return the evaluation of the current state according the cornes captured method
    def evaluationCornersCaptured(self):
        costBlack = 0
        costWhite = 0

        # Get the number of Black and White coins who are in the corners
        for lineCornerPos, columnCornerPos in [[0, 0], [0, self.boardSize-1], [self.boardSize-1, 0], [self.boardSize-1, self.boardSize-1]]:
            if self.current_state[lineCornerPos][columnCornerPos] == 'B':
                costBlack += 1
            elif self.current_state[lineCornerPos][columnCornerPos] == 'W':
                costWhite += 1
        if costBlack + costWhite == 0:
            return 0
        else:
            return 100 * (costBlack - costWhite) / (costBlack + costWhite)
