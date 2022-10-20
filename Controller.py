import sys
from Model import Game
from View import View


class Controller:

    # Constructor
    def __init__(self):
        self.game = Game()
        self.view = View()

    # Method to play the game

    def play(self):
        runGame = True
        while runGame:
            # Initialize the game by asking the player whether they want to play against a computer
            playerBlackType = self.view.askPlayerType("Black")
            if playerBlackType == 2:
                self.game.playerBlackHeuristic = self.view.askWantedHeuristic(
                    "Black")
                # Ask the search depth for the minimax algorithm if the heuristic is not random
                if self.game.playerBlackHeuristic != 1:
                    playerBlackMaxSearchDepth = self.view.askWantedSearchDepth(
                        "Black")
            playerWhiteType = self.view.askPlayerType("White")
            if playerWhiteType == 2:
                self.game.playerWhiteHeuristic = self.view.askWantedHeuristic(
                    "White")
                # Ask the search depth for the minimax algorithm if the heuristic is not random
                if self.game.playerWhiteHeuristic != 1:
                    playerWhiteMaxSearchDepth = self.view.askWantedSearchDepth(
                        "White")

            gameOver = False
            previousCouldPlay = True
            self.game.getNewBoard()
            self.view.draw_board(self.game.current_state, self.game.boardSize)

            while not gameOver:
                # Store all valid moves and the associated list of coins to flip
                allValidMoves = self.game.getValidMoves(
                    self.game.currentPlayer)
                if len(allValidMoves) != 0:
                    print("Player " + self.game.currentPlayer + "'s turn")
                    # Black player's turn
                    if self.game.currentPlayer == 'B':
                        # If the player is human ask the position where the player wants to play
                        if playerBlackType == 1:
                            (line, column, allCoinsToFlip) = self.view.askPlayerMoveWithMapOfValidMoves(
                                self.game.currentPlayer, allValidMoves, self.game.boardSize)
                        # If the player chooses the nect moove randomly
                        elif self.game.playerBlackHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.game.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.game.max(
                                0, playerBlackMaxSearchDepth, -sys.maxsize, sys.maxsize)
                    # White player's turn
                    else:
                        # If the player is human ask the position where the player wants to play
                        if playerWhiteType == 1:
                            (line, column, allCoinsToFlip) = self.view.askPlayerMoveWithMapOfValidMoves(
                                self.game.currentPlayer, allValidMoves, self.game.boardSize)
                        # If the player chooses the nect moove randomly
                        elif self.game.playerWhiteHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.game.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.game.min(
                                0, playerWhiteMaxSearchDepth, -sys.maxsize, sys.maxsize)

                    # Play the move by updating the board
                    self.game.playMoveWithListOfAllCoinsToFlip(
                        self.game.currentPlayer, line, column, allCoinsToFlip)

                    self.view.draw_board(
                        self.game.current_state, self.game.boardSize)
                    self.game.currentPlayer = self.game.getOppositePlayer(
                        self.game.currentPlayer)
                    previousCouldPlay = True

                # If the current palyer can not play, the plyer skip his turn
                else:
                    if (previousCouldPlay):
                        self.game.currentPlayer = self.game.getOppositePlayer(
                            self.game.currentPlayer)
                        previousCouldPlay = False
                    # If the prvious and the current player can not play, then the game is over
                    else:
                        gameOver = True
            # End of the game
            nbBlack, nbWhite = self.game.getScore()
            self.view.displayResult(nbBlack, nbWhite)

            # Ask the player if they want to play again
            print()
            playAgain = self.view.askPlayAgain()
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
            self.game.playerBlackHeuristic = playerBlackHeuristic
            self.game.playerWhiteHeuristic = playerWhiteHeuristic

            gameOver = False
            previousCouldPlay = True
            self.game.getNewBoard()
            # self.view.draw_board()

            while not gameOver:
                # Store all valid moves and the associated list of coins to flip
                allValidMoves = self.game.getValidMoves(
                    self.game.currentPlayer)
                if len(allValidMoves) != 0:
                    # print("Player " + self.game.currentPlayer + "'s turn")
                    # Black player's turn
                    if self.game.currentPlayer == 'B':
                        # If the player chooses the next moove randomly
                        if self.game.playerBlackHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.game.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.game.max(
                                0, playerBlackMaxSearchDepth, -sys.maxsize, sys.maxsize)
                    # White player's turn
                    else:
                        # If the player chooses the nect moove randomly
                        if self.game.playerWhiteHeuristic == 1:
                            (line, column, allCoinsToFlip) = self.game.chooseRandomMoveWithMapOfValidMoves(
                                allValidMoves)
                        # If the player is an AI, computes the next move
                        else:
                            (value, line, column, allCoinsToFlip) = self.game.min(
                                0, playerWhiteMaxSearchDepth, -sys.maxsize, sys.maxsize)

                    # Play the move by updating the board
                    self.game.playMoveWithListOfAllCoinsToFlip(
                        self.game.currentPlayer, line, column, allCoinsToFlip)

                    # self.view.draw_board()
                    self.game.currentPlayer = self.game.getOppositePlayer(
                        self.game.currentPlayer)
                    previousCouldPlay = True

                # If the current palyer can not play, the plyer skip his turn
                else:
                    if (previousCouldPlay):
                        self.game.currentPlayer = self.game.getOppositePlayer(
                            self.game.currentPlayer)
                        previousCouldPlay = False
                    # If the prvious and the current player can not play, then the game is over
                    else:
                        gameOver = True
            # End of the game
            nbBlack, nbWhite = self.game.getScore()
            # print("Player Black has " + str(nbBlack) + " coins and player White has " + str(nbWhite) + " coins.")
            if nbBlack > nbWhite:
                # print("Player Black wins!")
                nbWinBlack += 1
            elif nbBlack < nbWhite:
                # print("Player White wins!")
                nbWinWhite += 1
            else:
                # print("It's a tie!")
                nbDraw += 1

        print("For " + str(nbGames) + " games: player Black won " + str(nbWinBlack) +
              " times, payer White won " + str(nbWinWhite) + " times and there were " + str(nbDraw) + " draws.")
