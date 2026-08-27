import numpy as np
import pytesseract
import cv2 as cv
import queue


REDUCTION_KERNEL = 8
WHITE_THRESHOLD_PERC = 30
WHITE_THRESHOLD = REDUCTION_KERNEL**2 * WHITE_THRESHOLD_PERC // 100

class GameBoard:



    def __init__(self, capture, resizeDims=(484, 208)):
        self.resizeDims = resizeDims
        np_array = np.frombuffer(capture, dtype=np.uint8)
        self.originalCapture = cv.imdecode(np_array, cv.IMREAD_COLOR)
        self.mazeReduced = cv.resize(self.originalCapture, resizeDims, interpolation=cv.INTER_AREA)
        #self.captureStream = queue.Queue(5)

        self.pacLives = 3
        self.scoreCounter = 0

        self.readyCaption = True
        self.gameOverCaption = False
        self.cinematicPlaying = False

        self.charactersPos = {
            "Pacman": (0,0),
            "Pinky": None,
            "Blinky": None,
            "Inky": (),
            "Clyde": ()
        }

        self.compressedMat = np.zeros((self.mazeReduced.shape[0], self.mazeReduced.shape[1])) # 2-dimensional 'numpy.ndarray' representing mazeStructure


    def lifeLoss(self):
        self.pacLives -= 1

    def lifeWin(self):
        self.pacLives += 1

    def runTimeStepChecks(self):
        # check if cinematic playing, caption displaying...
        pass
        
    def encodeMaze(self): # or 'reduceMaze', or 'create'
        maze_croped = self.mazeReduced[44:172,14:470].copy()  # may want to change 44 by 42
        maze_hsv = cv.cvtColor(maze_croped, cv.COLOR_BGR2HSV)

        lower_yellow = np.uint8([0, 95, 5])  # 
        upper_yellow = np.uint8([25, 255, 255])

        pacgumsMask = cv.inRange(maze_hsv, lower_yellow, upper_yellow)



        lower_yellow = np.uint8([30, 250, 150])  # 
        upper_yellow = np.uint8([30, 255, 255])

        pacmanMask = cv.inRange(maze_hsv, lower_yellow, upper_yellow)
        combinedMask = cv.bitwise_or(pacgumsMask, pacmanMask)
        maskInversion = cv.bitwise_not(combinedMask)
        pacgumRemoved = cv.bitwise_and(maze_croped, maze_croped, mask=maskInversion)
        pacgumRemovedGray = cv.cvtColor(pacgumRemoved, cv.COLOR_BGR2GRAY)
        threshold, mythresh = cv.threshold(pacgumRemovedGray, 16, 255, cv.THRESH_BINARY)
        myMaze = cv.bitwise_and(pacgumRemoved, pacgumRemoved, mask=mythresh)

        myMazeCopy = myMaze.copy()
        cv.floodFill(myMazeCopy, None, (8,8), (0,0,255))

        lower_yellow = np.uint8([0, 0, 25])
        upper_yellow = np.uint8([0, 0, 255])

        frameThreshPac = cv.inRange(myMazeCopy, lower_yellow, upper_yellow)


        print(frameThreshPac.shape[0] // REDUCTION_KERNEL, frameThreshPac.shape[1] // REDUCTION_KERNEL)
        compressedMat = np.zeros((frameThreshPac.shape[0] // REDUCTION_KERNEL, frameThreshPac.shape[1] // REDUCTION_KERNEL), dtype=np.int8)


        #vérifier le nombre de pixel blancs dans un carré
        # associer un intervalle de l'image d'origine à un indexe de l'image compressée
        # SOIT range(0, frameThreshPac.shape[1], REDUCTION_KERNEL)
        # SOIT range(frameThreshPac.shape[1] // REDUCTION_KERNEL)
        # ALGORITHM : Write compressed matrix

        for X in range(0, frameThreshPac.shape[0], REDUCTION_KERNEL):
            for Y in range(0, frameThreshPac.shape[1], REDUCTION_KERNEL):
                currentKernel = frameThreshPac[X:X+(REDUCTION_KERNEL-1),Y:Y+(REDUCTION_KERNEL-1)]
                if np.count_nonzero(currentKernel == 255) >= WHITE_THRESHOLD: # si au moins 30% des pixels sont blancs, passer noir
                    compressedMat[X//REDUCTION_KERNEL, Y//REDUCTION_KERNEL] = 1
                else:
                    compressedMat[X//REDUCTION_KERNEL, Y//REDUCTION_KERNEL] = 0



        # Add black border around compressed version of the maze
        row, col = compressedMat.shape[:2]
        bottom = compressedMat[row-2:row, 0:col]
        mean = cv.mean(bottom)[0]

        borderSize = 1
        compressedMatBlackBorder = cv.copyMakeBorder(
            compressedMat,
            top=borderSize,
            bottom=borderSize,
            left=borderSize,
            right=borderSize,
            borderType=cv.BORDER_CONSTANT,
            value=0
        )

        
        # Add white pixels to allow pacman to use the flip side corridor
        compressedMatBlackBorder[compressedMatBlackBorder.shape[0]//2, 0] = 1
        compressedMatBlackBorder[compressedMatBlackBorder.shape[0]//2 - 1, 0] = 1
        compressedMatBlackBorder[compressedMatBlackBorder.shape[0]//2, compressedMatBlackBorder.shape[1] - 1] = 1
        compressedMatBlackBorder[compressedMatBlackBorder.shape[0]//2 - 1, compressedMatBlackBorder.shape[1] - 1] = 1

        self.compressedMat = compressedMatBlackBorder

    
    def update(self, capture):
        np_array = np.frombuffer(capture, dtype=np.uint8)
        self.originalCapture = cv.imdecode(np_array, cv.IMREAD_COLOR)

        self.mazeReduced = cv.resize(self.originalCapture, self.resizeDims, interpolation=cv.INTER_AREA)



        # Get textual elements from original image
        displayGameMsgImg = self.originalCapture[315:340,720:850]
        grayscaleimg = cv.cvtColor(displayGameMsgImg, cv.COLOR_RGB2GRAY)
        threshold, thresh = cv.threshold(grayscaleimg, 120, 255, cv.THRESH_BINARY_INV)
        displayedGameMsg = pytesseract.image_to_string(thresh)


        displayScoreImg = self.originalCapture[50:100,0:80]
        grayscaleScoreImg = cv.cvtColor(displayScoreImg, cv.COLOR_RGB2GRAY)


        # We use the fact that the area containing the score is completely black (only 0's matrix)
        # while the cinematic is playing which gives
        if(not np.any(self.originalCapture[50:100,0:120])): # this will be True, when the score area is fully black
            self.cinematicPlaying = True
        else:
            self.cinematicPlaying = False
            threshold, thresh = cv.threshold(grayscaleScoreImg, 100, 180, cv.THRESH_BINARY_INV)
            custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789' # tell pytesseract that it is expected to extract digits
            self.scoreCounter = pytesseract.image_to_string(thresh, config=custom_config)



        pacLives = cv.cvtColor(self.originalCapture[480:530, 25:150].copy(), cv.COLOR_BGR2RGB)
        grayscale = cv.cvtColor(pacLives, cv.COLOR_RGB2GRAY)
        ret, binary = cv.threshold(grayscale,127,255,cv.THRESH_BINARY)

        cnts,hierarchy = cv.findContours(binary,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        self.pacLives = len(cnts)





        # get characters location coordinates on compressed mat from reduced image


        maze_croped = self.mazeReduced[44:172,14:470].copy() 
        maze_hsv = cv.cvtColor(maze_croped, cv.COLOR_BGR2HSV)

        lower_yellow = np.uint8([25, 25, 198])  
        upper_yellow = np.uint8([35, 255, 255])

        pacmanMask = cv.inRange(maze_hsv, lower_yellow, upper_yellow)

        cnts,hierarchy = cv.findContours(pacmanMask,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        cnt = sorted(cnts, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cnt[-1])

        pacmanPosInReducedImage = (x + w//4, y + h//4)

       
        # The "+1" factor for both coordinates accounts for the black (1's) border we added around (on left and top edge)
        self.charactersPos["Pacman"] = (((x + w//4) // REDUCTION_KERNEL) + 1, ((y + h//4) // REDUCTION_KERNEL) + 1)




        # Blinky : the red ghost
        lower_red = np.uint8([0, 150, 200])  
        upper_red = np.uint8([0, 255, 255])

        blinky = cv.inRange(maze_hsv, lower_red, upper_red)
        cnts,hierarchy = cv.findContours(blinky, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        cnt = sorted(cnts, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cnt[-1])

        blinkyPosInReducedImage = (x + w//4, y + h//4)

       
        # The "+1" factor for both coordinates accounts for the black (1's) border we added around (on left and top edge)
        self.charactersPos["Blinky"] = (((x + w//4) // REDUCTION_KERNEL) + 1, ((y + h//4) // REDUCTION_KERNEL) + 1)


        # Pinky : the pink ghost
        lower_pink = np.uint8([165, 30, 220])  
        upper_pink = np.uint8([165, 255, 255])

        pinky = cv.inRange(maze_hsv, lower_pink, upper_pink)
        cnts,hierarchy = cv.findContours(pinky,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        cnt = sorted(cnts, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cnt[-1])

        pinkyPosInReducedImage = (x + w//4, y + h//4)

       
        # The "+1" factor for both coordinates accounts for the black (1's) border we added around (on left and top edge)
        self.charactersPos["Pinky"] = (((x + w//4) // REDUCTION_KERNEL) + 1, ((y + h//4) // REDUCTION_KERNEL) + 1)


        # Inky : the blue ghost
        lower_blue = np.uint8([90, 50, 150])  
        upper_blue = np.uint8([90, 255, 255])

        inky = cv.inRange(maze_hsv, lower_blue, upper_blue)
        cnts,hierarchy = cv.findContours(inky,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        cnt = sorted(cnts, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cnt[-1])

        inkyPosInReducedImage = (x + w//4, y + h//4)
   
        # The "+1" factor for both coordinates accounts for the black (1's) border we added around (on left and top edge)
        self.charactersPos["Inky"] = (((x + w//4) // REDUCTION_KERNEL) + 1, ((y + h//4) // REDUCTION_KERNEL) + 1)



        # Clyde : the orange ghost
        lower_orange = np.uint8([22, 50, 150])  
        upper_orange = np.uint8([23, 255, 255])

        clyde = cv.inRange(maze_hsv, lower_orange, upper_orange)
        cnts,hierarchy = cv.findContours(clyde,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        cnt = sorted(cnts, key=cv.contourArea)
        x,y,w,h = cv.boundingRect(cnt[-1])

        clydePosInReducedImage = (x + w//4, y + h//4)

       
        # The "+1" factor for both coordinates accounts for the black (1's) border we added around (on left and top edge)
        self.charactersPos["Clyde"] = (((x + w//4) // REDUCTION_KERNEL) + 1, ((y + h//4) // REDUCTION_KERNEL) + 1)



        for character, pos in self.charactersPos.items():
            if(self.compressedMat[pos[0],pos[1]] == 0):
                print(character + " is in start zone")
                self.charactersPos[character] = None

        # penser à vérifier si le résultats tombe sur une case qui vaut 1 (pour le cas où les fantômes sont dans la cage) sinon, attribuer
        # la valeur None, (à voir si c'est vraiment nécessaire ?? je pense pas forcément, pcq seul Pacman est concerné par les cases autorisées)
        # ou alors décider que un fantôme en cage se trouve directement sur les coordonnées valides devant la porte de la cage





        # print(w,h)


        


    def setCinematicPlaying(self): 
        # We use the fact that the area containing the score is completely black (only 0's matrix)
        # while the cinematic is playing which gives
        if(not np.any(self.originalCapture[50:100,0:120])): # this will be True, when the score area is fully black
            self.cinematicPlaying = True
        else:
            self.cinematicPlaying = False



    def getPacmanPos(self):
        return self.characterPos["Pacman"]
    
    def setPacmanPos(self):
        # self.mazeReduced
        # detect
        self.characterPos["Pacman"]
    
    def setGameStatusCaption(self):
        pass
        """
        displayGameMsgImg = testimage[315:340,720:850]
        grayscaleimg = cv.cvtColor(displayGameMsgImg, cv.COLOR_RGB2GRAY)
        threshold, thresh = cv.threshold(grayscaleimg, 120, 255, cv.THRESH_BINARY_INV)
        displayedGameMsg = pytesseract.image_to_string(thresh)
        if("GAME OVER" in displayedGameMsg.strip().upper()):
            self.gameOver = True
        elif("READY" in displayedGameMsg.strip().upper()):
            self.readyCaption = False
        else:
            print("No caption available, the game is running")
        """


    def getGameStatusCaption(self, capture):
        displayGameMsgImg = capture[315:340,720:850]
        grayscaleimg = cv.cvtColor(displayGameMsgImg, cv.COLOR_RGB2GRAY)
        threshold, thresh = cv.threshold(grayscaleimg, 120, 255, cv.THRESH_BINARY_INV)
        return pytesseract.image_to_string(thresh)
    
    def getOriginalCapture(self):
        return self.originalCapture
    
    def getResizedCapture(self):
        return self.mazeReduced
    
    def setNewCapture(self, capture):
        np_array = np.frombuffer(capture, dtype=np.uint8)
        self.originalCapture = cv.imdecode(np_array, cv.IMREAD_COLOR)
        self.mazeReduced = cv.resize(self.originalCapture, self.resizeDims, interpolation=cv.INTER_AREA)

    
    def enqueue(self, cap):
        if(not self.captureStream.full()):
            np_array = np.frombuffer(cap, dtype=np.uint8)
            self.bufferStream.put(cv.imdecode(np_array, cv.IMREAD_COLOR))
        else:
            print("Stream buffer is full")

    def dequeue(self, cap):
        if(not self.bufferStream.empty()):
            return self.bufferStream.get()
        else:
            print("Buffer empty !")




    def getLivesCount(self):
        return self.pacLives
    

    def getCompressedMat(self):
        return self.compressedMat


    def __str__(self): # , showImageInSeparateWindow=False  if showImageInSeparateWindow:
        
        
        #cv.imshow("Compressed maze", self.compressedMat)
          
        output = ""
        for X in range(self.compressedMat.shape[0]): 
            for Y in range(self.compressedMat.shape[1]):
                output += "{:>2}".format(self.compressedMat[X, Y])
                
            output += "\n"

        output += "Remaining lives : {}\n".format(self.getLivesCount())
        return output
        #print("Score : ", self.getScore())
        #print("Remaining lives : ", self.getLivesCount())
        #print("Compressed Mat dimensions ", str(self.compressedMat.shape[0]) + " " + str(self.compressedMat.shape[1]))

        #cv.waitKey(0)
        #cv.destroyAllWindows()

        
    