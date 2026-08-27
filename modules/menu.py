

class Menu:

    def __init__(self):
        self.QUIT = False

    def welcome_or_display():

        # Nice method/way to emulate switch-case behaviour which exists in other programming languages
        # but is not available in Python (see Python book chap?)

        print("------------WELCOME IN PACMAN SOLVER--------------")
        print("Type 'q' to leave")
        print("Algorithm to experiment :")
        print("1. Dynamic programming (iterative method for solving the planning problem using Bellman equation i.e, no interaction with the env : stationnary problem)")
        print("1. Monte Carlo (a priori x 1st visit MC)")
        print("2. Monte Carlo (a posteriori x every visit MC)")
        print("2. SARSA")
        print("2. TD-Learning")
        print("2. Q-learning")
        print("3. Deep Q-learning")
        print("4. Imitation Learning")

    def loadAlgo(self, algoId_str):
        # Switch-case alternative using a python dictionnary
        algoId = int(algoId_str)
        algoSelect = {
            0: DP,
            1: aprioriMC,
            2: aposterioriMC
        }

        if (algoId in algoSelect.keys()):
            # return instance of selected algo
            return algoSelect[algoId]()



    def quit(self):
        print("Do you want to quit ? ('y' or 'n')")
        userChoice = int(input())
        if userChoice == 'y':
            self.QUIT = True

