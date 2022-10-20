class View:

    # Get an input of type int between min and max value
    # Return a correct input
    def getIntInput(self, minValue, maxValue):
        correctInput = False
        while not correctInput:
            try:
                value = int(input())
                if value < minValue or value > maxValue:
                    print("Invalid input. The number must between " +
                          str(minValue)+" and "+str(maxValue)+".")
                else:
                    correctInput = True
            except ValueError:
                print("Invalid input. Please enter a number.")
        return value

    # Draws the board
    def draw_board(self, board, boardSize):
        for line in range(boardSize+1):
            for column in range(boardSize + 1):
                if line == 0:
                    if column == 0:
                        print(end=" ")
                    else:
                        print(" " + str(column-1), end='')
                else:
                    if column == 0:
                        print(line-1, end='')
                    else:
                        print('|%s' %
                              (board[line-1][column-1]), end='')
            if line != 0:
                print('|')
            else:
                print()
        print()

    # Display the winner of the game dependifng on the result
    def displayGameResult(self, nbBlack, nbWhite):
        print("Player Black has " + str(nbBlack) +
              " coins and player White has " + str(nbWhite) + " coins.")
        if nbBlack > nbWhite:
            print("Player Black wins!")
        elif nbBlack < nbWhite:
            print("Player White wins!")
        else:
            print("It's a tie!")

    # Ask the player whether he wants to play as a human or as an AI
    # Return 1 if human, 2 if AI
    def askPlayerType(self, playerColor):
        print("The player " + str(playerColor) + " is: ")
        print("1) Human")
        print("2) AI")
        return self.getIntInput(1, 2)

    # Ask the player to choose the heuristic he wants to play whith
    # Return the chosen heuristic
    def askWantedHeuristic(self, playerColor):
        print("Please select the heuristic for player " + str(playerColor))
        heuristicType = ["Random", "Static", "Corners captured"]
        for index in range(len(heuristicType)):
            print(str(index+1) + ") " + str(heuristicType[index]))
        return self.getIntInput(1, len(heuristicType))

    # Ask the player how deep he wants to search
    # Return the depth (must be between 1 and 10)
    def askWantedSearchDepth(self, playerColor):
        print("Please select the search depth for player " +
              str(playerColor) + " (max. recomended 7)")
        return self.getIntInput(1, 10)

    # Ask the players whether they want to continue to play
    # Return a boolean saying whether the players want to continue to play
    def askPlayAgain(self):
        print("Do you want to play again?")
        print("1) Yes, of course!")
        print("2) No thanks")
        return self.getIntInput(1, 2)

    # Ask the player the position where he wants to play until it is a valid one
    # Return line, column, allCoinsToFlip : a valid position where the player wants to play and the associated list of coins to flip
    def askPlayerMoveWithMapOfValidMoves(self, currentPlayer, validMoves, boardSize):
        validMove = False
        while not validMove:
            print("Player " + currentPlayer + " where do you want to play?")
            print("Line:")
            line = self.getIntInput(0, boardSize)
            print("Column:")
            column = self.getIntInput(0, boardSize)
            value = validMoves.get(
                str(line)+","+str(column))
            if not value:
                print("Invalid move.")
            else:
                validMove = True
        return line, column, value[2]
