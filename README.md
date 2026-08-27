# PacmanSolver

This project is part of my application at ...

The purpose of this project is to demonstrate my knowledge on various technical topics and skills working along with essential tools powering the world of modern AI. It is intended to demonstrate my ability to collaborate and bring contribution to open-source research projects. What follows comes with the aim to showcase various algorithms, techniques, RL skills and PyTorch knowledge. This project is published under MIT License. Feel free to reach out for any complementary information or remarks. Any suggestion is highly appreciated. 

Happy reading/Enjoy !


outline/Table of contents

Setup guide
1. Game Modeling (theory) (May be the most difficult because various ways of modeling, but also may be the most important)
2. Major Milestones (implementation)
3. Result analysis

## Quick setup guide

## Key hilights

* Point 1
* Point 2
* ...
* Point 3

## About

Step 1 : Présentation du jeu (historique de pacman)

Pac-Man, released by Namco in 1980, is one of the most iconic and influential arcade games of all time. Created by Toru Iwatani, this maze-chase game introduced players to a simple yet addictive concept: navigate Pac-Man through a labyrinth, eating dots while avoiding colorful ghosts—Blinky, Pinky, Inky, and Clyde. With its vibrant graphics, catchy soundtrack, and innovative gameplay, Pac-Man not only defined the golden age of arcade gaming but also became a cultural phenomenon, transcending its medium to appear in movies, TV shows, and even as a symbol of pop culture. Its timeless appeal lies in its perfect blend of strategy, speed, and charm, making it a staple in retro gaming collections worldwide.

If you know the game and have ever played, have you ever felt the frustration of never completing/undergoing more than the third level ? (this was my case, but) With this project, that time will be over.
####### No more title level available

--> Présentation Jeu (historique de pacman)/ Présentation Pacman
--> Convenience of this choice 
--> Justification de la pertinence du projet (influence de la résolution de labyrinthe dans l'avancée du RL et de l'IA en général)
Progrès et influence de la résolution de labyrinthe dans l'Histoire du RL


Explain what is a Google Doodle. First Doodle of the history of the Doodle events to be interactive.

This program uses the [Google Doodle](https://www.google.com/logos/2010/pacman10-i.html) version of the game released for its 30th anniversary. The Google Doodle game will be very convenient for us since it is directly accessible from any web browser. It requires no extra install. 

It requires no additional coding for implementing the game, so that it enables to focus all our attention on the problem solving issues. In addition, it will be easilly controllable through browser automation tools. The game is well known or at least its rules are easily understandable by anyone and the action set of available interaction possibilities is relatively limited/small.


Maze solving systems have played a significant role in the improvment/progress of those algorithms. / are responsible of great improvments
Maze solving has played a significant role in discoveries and progress in RL litterature and in a broader extent to AI algorithms.

Exemple d'utilisation du RL dans la résolution de labyrinthes (S&B p38)
Many promising applications... applicable to a broad range of domains.
But tremendous progress in the field those last ten years.
More recently (2015), in the Neurex Conference (major ML conference), David Silver from Google Deep mind presented breathtaking results of the use of RL to control Atari games (DeepMind, Nature, 2015). For instance, he succeeded to solve "Breakout" games with algorithms that were directly fed from pixel input.
+ and Atari games later on.
Pacman is a maze-based atari game in which the player...


imitation learning : increasing importance (Andrew Ng helicopters)


ROI (Region Of Interest) extraction, OCR (Optical Character Recognition)



## Quick setup guide























Let's briefly tackle common RL concerns and challenges in the context of the Pacman solving problem :

## Main concerns

  ### Game modelisation

  ### Point of view



## Menu hilights

## Step 1 : Presentation and configuration

## Step 2 : Game modelization

Pacman board :

For each individual pixel, gameboard in a matrix :

* walls are represented by 'w' character
* our own character (pacman) is represented by 'p'
* gosts are represented by 'g' (knowing that each has a different "personality", do we differentiate them ?)

The matrix describing maze structure, could define dimensions from distance travelled while maintaining a directionnal key during 1s

Let's now dive deeper into the game mechanics. 

Gameboard modelization

* Raw pixel input
* In-matrix modeling
* Reduced matrix modelling (using floodfill algo)

--> matrix where only places where pacman can go are considered as "states" --> MDP graph --> MDP adjacency matrix


Think about your litterature courses back in high school.
In litterature, a point of view is the perspective in which the narrator places itself to tell the story. Being omniscient means that he knows everything about any action occuring anywhere and implicating any character.
Agent (Pacman) point of view (pov) can be :

* Omniscient (the agent has a complete knowledge of the environment in which it operates)
* Internal (sensitive/perceptible/noticeable)


In RL, this notion is about to compare the world state wrt the agent state.
When both are the same, which is s_t=o_t we talk about "full observability" and we lie in the case of Markov decision processes (MDP) (also called "complete knowledge")
When they are different, we fall in the "partial observability" problem Partially Observable Markov Decision Processes (POMDP)
(also called "incomplete knowledge")

(Pas exactement "complete" and "incomplete" knowledge fait référence à l'existence ou non d'un modèle parfait de transition/dynamique de l'environnement)



indefinite horizon : the pacman game will end but we don't know when --> "model as infinite horizon and look at the probability of reaching termination states" (58:00 CS234 course 1)

## Game mechanics description / game vocabulary 
(importance du caractère non aléatoire et des personnalités attribuées aux fantômes)
An important point is that ghosts moves are not assigned completely randomly. The game creator wanted to assigned to characters kind of personalities resulting in them behaving following with pre-defined strategies. This is a foundamental assessment for our interpretation, analysis and subsequent choices of modelization.

Once we stated that, many questions arises in terms of modelization choices ?

* Agent pov ?
* Do we differentiate ghosts or not ?





à la fin (chap results analysis) essayer de faire un tableau : choix de modelisation vs algorithmes qui affiche les différentes métriques associées + des graphiques pour chacun.


## Game domain specific encoding / Representational choice
Representational choice is decisive issue for our algorithms to perform well but are describe more as an art than a science (S&B)


## Theory/use case mapping  -  conceptual mapping  -  Conceptual analysis of the game

make UML diagram (class diagram) to depict my code architecture hilighting main game concepts.

* class GameBoard
* class Level (has a GameBoard)


This problem could be hardly framed as an AI planning problem : large state space, planning does not involve interaction with environment


keyconcepts of RL :

**What is an agent ?**

The Agent is the part of our program deciding actions

**What is the environment ?**

The environment is the image representing the gameboard




Definition of the S, A, R triplet
**What are states ?**

The states are each position on the gameboard where pacman can move

**What are actions ?**

Actions are the set : arrow up, arrow down, arrow right, arrow left, do nothing

Sampling/action selection can be done : 

1) At fixed frequency 
2) Just before each intersection

Associativeness ?
With the Pacman game we are in a "non-associative" setting, that is there is a single action space shared among every input state (currently parsed Gameboard configuration) ???? NO
--> Associative means that the optimal action is not the same from each state, which is the case in Pacman. Pacman IS associative.

Stationnarity ?
The problem is not stationnary since the reward distribution may change at any time based on ghosts moves.


The PacMan game is associative and non-stationnary.

Problem is finite because S, A and R are finite sets

Remark that the result of a "go left" action is strictly equivalent to a "do nothing" action while pacman is already going left.


**What are rewards ?**

Rewards are the points won while reaching pacman game sub-goals
Negative rewards affect this score when pacman is hit by a ghost (loose single life) and loose a whole game 


Modeling rewards for maintaining max distance to ghost (safe strategy): somme des distances séparant pacman de tous les fantômes (normalisé par le nombre de cases traversables)

Agent goals can be defined in many different ways, it can be for example :

* Score focused : Maximizing overall score (Metric : newScore - oldScore)
* Level completion focused : eating all "pacgums" as fast as possible without being eaten. (pacman in a hurry)
* Survival focused : The timid pacman (try to maximize its distance to ghosts)

In my opinion, the first option represents the best indicator since it covers/captures the two aspects below into a single metric. Completing the maze quickly does not constitute in itself a guaranty to survive, while the pacman only focused to escape ghosts may keep stuck in a level for hours without completing it.
In any case (any of the option choosen between the two above), hitting a ghost (represented by monitoring the loss of "life icons") will result in loosing
**What does *"winning"* means in the context of Pacman ? How do we win points ?**

* Eating ghosts
* Eating fruits
* Eating "dot pacgums"
* The three action above results in raising score at the top left corner of the maze
* Completing two level results in playing a short animation

The ultimate goal of the Pacman game is to raise a counter by collecting diverse items known as "pacgums". Here, we will not worry about the different sub-goals enabling to gain points since solving one maze is independent from keeping up earning point
It has no connection from one level to another.

As stated in S&B,
S&B expliquent que la notion de victoire doit être attribuées au but recherché et non à la résolution de "sous-problèmes" censés amenés à la victoire (supposed to convey victory on the long run):
It is clearly stated in S&B that the definition of a win.../ should be only driven by the ultimate goal of the agent and not by intermediary achievements or "subgoals"/subtasks solving (S&B, chap 3.2, p 76/54)

reward signals should be attributed or assigned on the basis of...

Au contraire, (p56, Exo 3.7), ils disent que la récompense peut être émise pour des accomplissements successifs ou bien à la toute fin de la résolution du labyrinthe ?!

Many ways of framing the concept of "reward" for this problem, we could deine negative rewards while cells separating pacman from ghosts decreases.


**What about *"loosing"* ?**

* Loosing a life : disappearance of one life instance icon in bottom left corner
* "Game Over" is displayed


Set of actions is relatively simple. It is the set of 4 arrows {top, right, bottom, left} or card(A) = 5 :{top, right, bottom, left, noactions}

or for each S_t, the action space is defined as a subset of {top, right, bottom, left} accordingly to the S_t+1 state accessibility

//Note that given a current state, the action space can be a subset of this space

## Major milestones

### Step 1 : Discovery of the maze structure

## Algorithm flow

--> At program launch, a CLI menu is prompting with which algorithm I want to launch a game
--> Once the algorithm is chosen, if it is the first time launching this option, it immediatly starts in training mode. Otherwise, the user is asked to either launch a training phase or enter in testing phase benefitting from previous trainings. (exploit previous training acquired knowledge)
--> Launch game in browser
--> Take snapshots of the gameboard (at X Hz)
--> Croping and resizing the game board if necessary (reduce computationnal requirements + image of the current state should be localized strictly in the same frame for the algorithm to run smoothly)
--> Detect and crop ROI (Region of interests) like pacman and ghost frame position in the MAZE
--> Perform extra cleaning and encoding if necessary
--> Reward is attributed on the basis of win detection (via OCR on the score and other techniques)
--> Penalties are attributed each time the "remaining life" counter is decreasing or the game is over
--> loop through many games



Markov assumption : the current state is a sufficient statistic of the history, that is : p(s_(t+1)|s_t, a_t) = p(s_(t+1)|h_t,a_t)
We make MDP assumption

## Algorithm tested

Planning (CUDA + row reduction)
https://stackoverflow.com/questions/67339113/can-pca-be-used-for-row-reduction

PCA is for Components/Variables (aka column reduction), the equivalent to row reduction is segmentation/clustering (hierachichal clustering, dbscan, kmeans sur les scores) + utilisation de tree structure dans l'enregistrement sur un principe fréquentiels des scores de désirabilité résumé (comme dans le cas de Huffman).


Monte-Carlo 
TD-learning
Imitation learning
Q-learning
Deep Q-learning : Our algorithm will be fed directly from pixel input. (DeepPacman)





## Algorithms results analysis

Benchmark configuration

Before going into complex metrics, I can analyze the results from my own observations and experience (best personal score : 20470)

Notre score de référence correspond au record du monde du jeu par une être humain, on va voir si on peut s'en rapprocher voire l'égaler :

"
En 1999, l’Américain Billy Mitchell devient le premier joueur à avoir réalisé le score parfait de 3 333 360 points dans le jeu[15]. Il a terminé les 256 niveaux en six heures, attrapant tous les fruits, mangeant les quatre fantômes à chaque bonus, et ne perdant aucune vie à chaque niveau. 
"

256th level glitch


Economic aspects of simulation
## Others

Taking a screenshot with playwright/puppeteer
DVC for model version management

























































## References

(DeepMind, Nature, 2015)

### Writing bibliographies in GFM
https://stackoverflow.com/questions/26587527/cite-a-paper-using-github-markdown-syntax

### Pacman arcade game
https://fr.wikipedia.org/wiki/Pac-Man
https://en.wikipedia.org/wiki/Pac-Man
https://en.wikipedia.org/wiki/Pac-Man_Google_Doodle


### Markov chains
https://www.youtube.com/watch?v=LDiklt4dV24&pp=ugUHEgVlbi1HQg%3D%3D

veritasium
https://www.youtube.com/watch?v=KZeIEiBrT_w&pp=ygUNbWFya292IGNoYWlucw%3D%3D

partie 1
https://www.youtube.com/watch?v=i3AkTO9HLXo&pp=ygUNbWFya292IGNoYWlucw%3D%3D
partie 2
https://www.youtube.com/watch?v=VNHeFp6zXKU&pp=ugUEEgJlbg%3D%3D

### Reinforcment learning fundamentals
Sutton & Barto 2nd edition

Standord CS234, Emma Brunskill
[Stanford CS234: Reinforcement Learning | Winter 2019 | Lecture 1 - Introduction - Emma Brunskill](https://www.youtube.com/playlist?list=PLoROMvodv4rOSOPzutgyCTapiGlY2Nd8u)

[Stanford CS234 Reinforcement Learning I Introduction to Reinforcement Learning I 2024 I Lecture 1](https://www.youtube.com/playlist?list=PLoROMvodv4rN4wG6Nk6sNpTEbuOSosZdX)

[Stanford CS224R Apprentissage par renforcement profond | Printemps 2025 | Cours 1 : Introduction](https://www.youtube.com/playlist?list=PLoROMvodv4rPwxE0ONYRa_itZFdaKCylL)

https://web.stanford.edu/class/cs234/


Olivier Sigaud yt channel RL playlist
Chaine yt Mutual Information


[CUDA computing course](https://www.youtube.com/watch?v=86FAWCzIe_4)
[CUDA vs multiprocessing](https://www.digitalocean.com/community/tutorials/parallel-computing-gpu-vs-cpu-with-cuda)

### Deep learning fundamentals
Lex Friedmann neural networks

### Technologies
Browser automation : Playwright ou Puppeteer
Deep Learning : PyTorch

### More exemples of cybernetics and early RL systems trials




https://cyberneticzoo.com/mazesolvers/

Bristol's Robot Turtoises (Elmer & Elsie) : William Grey Walter (1950)

https://www.youtube.com/watch?v=t1pL5DrJ5rI
https://www.youtube.com/watch?v=wQE82derooc


electromecanical mouse
Maze running mouse (Theseus), Claude Shannon (1951)


https://www.youtube.com/watch?v=_9_AEVQ_p74


https://mitmuseum.mit.edu/collections/object/2007.030.001
https://www.technologyreview.com/2018/12/19/138508/mighty-mouse/

https://historyof.ai/shannon/


Précurseur des compétitions "micromouse": https://fr.wikipedia.org/wiki/Micromouse
https://en.wikipedia.org/wiki/Maze-solving_algorithm




Maze solving machine, Deutsch (1953)


French (cybernétique)
Electronic Fox : Albert Ducrocq     https://www.youtube.com/watch?v=rtv-X6yUmGg
Zebulon : Bruno Lussato