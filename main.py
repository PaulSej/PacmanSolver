from playwright.sync_api import sync_playwright
import modules.gameboard
import os
import pytesseract
import multiprocessing
import platform
import base64
import queue
import numpy as np
import itertools
import matplotlib.pyplot as plt
import random

import timeit
# print("random.choice:", timeit.timeit(funcName, setup="global bigset", number=10000))
class Main:

    def main():
        # Check platform and add correct binary/executable path for pytesseract lib for windows
        # equivalent to :   (os.name == "nt")
        if platform.system() == "Windows":
            pytesseract.pytesseract.tesseract_cmd = r'C:\Users\20190511\AppData\Local\Programs\Tesseract-OCR\tesseract'


        """
        ITER = 10000

        episode = 0
        while episode < ITER:
        """
    
        with sync_playwright() as p:
            try:  
                browser = p.firefox.launch(headless=False)
                page = browser.new_page() # no_viewport=True
                page.goto("https://www.google.com/logos/2010/pacman10-i.html")

    
                
                print(page.title())


                
                # generated with codegen:      playwright codegen https://www.google.com/logos/2010/pacman10-i.html
                
                
                ## Switch of sound :      #hplogo > div:nth-child(2)
                
                ## then while "ready" is dislayed wait
                ## create buffer class or use the "playwright buffer" ?
                gameHasStarted = False
                mazeLoaded = False
                while not gameHasStarted: # Tant que "Ready" est affiché
                    ## page.locator("#i").content_frame.get_by_title("").screenshot(path="./tests_folder/my_capture.png")
                    ## page.frame_locator("iframe").get_by_title("").screenshot(path="./tests_folder/my_capture.png")
                    capture = page.locator("#i").content_frame.get_by_title("").screenshot()
                    #print(type(base64.b64encode(capture).decode()))
                    #nparr = np.fromstring(base64.b64encode(capture), np.uint8)
                    
                    ## Prochaine étape : être capable de gérer, stocker envoyer les screenshots
                    if not mazeLoaded:
                        gameboard = modules.gameboard.GameBoard(capture)
                        gameboard.encodeMaze()
                        mazeLoaded = True

                    #gameboard.enqueue(capture)
                    gameboard.setNewCapture(capture)
                    if("READY" in gameboard.getGameStatusCaption(gameboard.getOriginalCapture()).strip().upper()):
                        gameHasStarted = True

                    page.wait_for_timeout(500)
                
                page.locator("[id=\"i\"]").content_frame.locator("#hplogo div").click() # switch sound off

                """
                # save and encode screenshot to variable
                screenshot_bytes = page.screenshot()
                print(base64.b64encode(screenshot_bytes).decode())

                
                # create a buffer (a buffer is a queue with limited size)

                buffer = queue.Queue(5)
                # Main available operations
                buffer.put() # add element
                buffer.get() # get element
                buffer.empty() # True when queue is empty
                buffer.full() # True when queue is full

                """
                # Once the game begin
                """
                TIMESTEP_SAMPLING_FREQ = 1000
                actions = {"ArrowLeft", "ArrowUp", "ArrowRight", "ArrowDown"}
                while(not gameboard.gameIsOver()):
                    capture = page.locator("#i").content_frame.get_by_title("").screenshot()
                    gameboard.update(capture)
                    print(gameboard)
                    selectedAction =  random.choice(list(actions))
                    page.keyboard.press(selectedAction)
                    page.wait_for_timeout(TIMESTEP_SAMPLING_FREQ)
                """


                
                
                
                """   
                page.wait_for_timeout(1000)
                page.keyboard.press("ArrowLeft")
                page.wait_for_timeout(2000)
                page.keyboard.press("ArrowUp")
                page.wait_for_timeout(2000)
                page.keyboard.press("ArrowLeft")
                page.wait_for_timeout(1000)
                page.keyboard.press("ArrowUp")
                page.wait_for_timeout(100)
                ## page.locator("#i").content_frame.get_by_title("").screenshot(path="./tests_folder/ingamecapture.png")
                page.keyboard.press("ArrowLeft")
                page.wait_for_timeout(5000)
                print(gameboard) # , showImageInSeparateWindow=True
                ## Attendre que Ready Disparaisse
                ## Puis dès qu'elle disparait, initialiser GameBoard
                """





            except TimeoutError:
                print("Did not succeed to capture the game board")
            else:
                ## Voir PlayWright docs > Getting Started - Library > Known issues > "time.sleep() leads to outdated state"
                ## Use page.wait_for_timeout(5000) instead of time.sleep(5)
                print("End browser the clean way !")
            finally:
                #context.close()
                browser.close()


        




            """
            QUIT = False
            MIN_TRAIN_ITERATION = 1000
            #On veut que :

            #* Notre programme boucle tant qu'il n'est pas stoppé par la commande 'q'
            #* Vérifier que l'utilisateur demande bien un algorithme qui est dispo (est dans l'intervalle de num correct)
            #* Pour l'exploitation des résultats, il y ait bien eu une session d'entrainement enregistrée au préalable
            # * Sécuriser les entrées contre les types de données inadaptés de l'utilisateur (str au lieu de int et vice versa)

            # * Do you want do train a "score focused" or a "level completion focused" agent ?
            while not QUIT:    

                # while algoChoice is Invalid         
                    print("Which algo do you want to test ?")

                    print("1. Algo 1")
                    print("2. Algo 2")
                    print("3. Algo 3")

                    algoChoice = int(input()) # pas int pour laisser la possibilité de saisir 'q'

                    


                    # à remplacer par quelque chose du style
                    # algo = Menu.loadAlgo(algoChoice) return instance of algo class for example "Monte-Carlo"
                    if(algoChoice != 'q'):
                        if(algoChoice == 1):
                            print("run algo 1")

                        elif(algoChoice == 2):
                            print("run algo 2")

                        elif(algoChoice == 3):
                            print("run algo 3")

                        else:
                            print("algorithm not available")
                    else:
                        break

                # While program mode is invalid

                    print("Train or Test ?")
                    print("1. Train the agent")
                    print("2. Exploit agent knowledge")

                    algoMode = int(input())


                    # if train mode, then ask iteration number (should be at least threshold (1000))
                    if(algoMode != 'q'):
                        if((algoMode == 1) or (algoMode == 2)):
                            print(algoMode)
                            # if algoMode == 2 and algo.wasTrained() ==  False
                                            
                        else:
                            print ("Please choose a valid mode")
                    else:
                        break


                    # print("The model will be written in " + str(modelFileName) + " but a model is already saved in this file")
                    # print("Do you want to overwrite it ? ('y' or 'n')")
                    # print("Model saved in " + str(modelFileName) + " with success !")









"""


    """
        menu = Menu()
        while not menu.QUIT:
            
            menu.welcome()

            # Do you want to train or test

            game.launch(algorithmchoice)
            if "training":
                pass


            if "testing":

            context

            QUIT = menu.quit()
    """




if __name__ == "__main__":
    Main.main() # Class method call
    # main = Main() # Instance method call
    # main.main()