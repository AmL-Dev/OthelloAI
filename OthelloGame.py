from Controller import Controller


class OthelloGame:

    # Constructor
    def __init__(self):
        self.controller = Controller()
        # self.controller.autoPlay(10, 2, 2, 1, 1) #To test the game with two AIs without going through the interface
        self.controller.play()


game = OthelloGame()
