import pygame
from squareFaster import square
import time


#CONWAY'S GAME OF LIFE:
#Cells can be alive or dead: red or white
#they must obey certain conditions:
#1: Every living cell with less than two adjacent living cells dies, by effect of loneliness.
#2: Every living cell with more than three adjacent living cells dies, by effect of over population.
#3: Every living cell with two or three adjacent living cells lives.
#4: Every dead cell surrounded by exactly three adjacent cells lives, by effect of reproduction.

#In this Pygame version, an Ascii map of the grid is included where the ones denote an alive cell
#and zeroes denote a dead cell.
#However the map is present only in the middle 25x25 cells so that it can be visible from the console.


#start: 19/04/2019
#end: 21/04/2019 (because of debugging...)

###################################################################################################


pygame.init()
WinBounds = 1501

win = pygame.display.set_mode((WinBounds,WinBounds))

pygame.display.set_caption("Conway's Game of Life")
bg = pygame.image.load("white.png")
clock = pygame.time.Clock()

#various starting variables
run = True
ready = False
start = False
showMap = False

#the boundaries of the square containing all of the living cells 
xSquareMin = WinBounds
ySquareMin = WinBounds
xSquareMax = 0
ySquareMax = 0

#all of the squares
squares = []

#all of the vertical sections occupied by a square or not (only for map)
occupiedSections = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
map = []

def redrawGameWindow():
    win.blit(bg,(0,0))
    
    # if the cycle starts then draw the square
    if start:
        for square in squares:
            square.draw(win)
    
    pygame.display.update()
    
def updateMap():

    for square in squares:
        
        #finds the y-section of the grid
        section = int(square.yPos/20)
        
        #finds the x-slot of the grid
        slot = int(square.xPos/20)
        
        #replaces the 0 with a 1 depending on the section and slot
        map[section] = map[section][0:slot] + "1" + map[section][slot+1:len(map[section-1])]


def checkAdjacentSquares(surface,xPos,yPos):
    
    #we don't take in consideration the middle square
    count = -1
    
    for i in range(3):
        xSquarePos = xPos - 30
        
        for j in range(3):
            #we use the middle of the square to avoid ambiguities
            
            xSquarePos += 20
            ySquarePos = 20*i + yPos - 10
            
            #if they are between the windows' border
            if ( WinBounds - 1 > xSquarePos > 0 and WinBounds-1 > ySquarePos > 0):
                #And are red then increment the count
                if surface.get_at((xSquarePos,ySquarePos))[0] == 255:
                    count += 1


    return count


while run:
    
    #resetting the boundaries
    xSquareMin = WinBounds
    ySquareMin = WinBounds
    xSquareMax = 0
    ySquareMax = 0
    
    #used to get the fps
    starty = time.time()
    clock.tick(20)
    
    #get the mouse position
    xCursor, yCursor = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        #if clicking on the red cross stop running
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            
            start = True
            
            #placing the square on the grid using modulus
            newXCursor = xCursor - xCursor%20
            newYCursor = yCursor - yCursor%20
            
            squares.append(square(newXCursor,newYCursor,0,(255,0,0)))
            
            
    keys = pygame.key.get_pressed()
    
    #if ESC is pressed then stop running
    if keys[pygame.K_ESCAPE]:
        run = False
    
    #waiting for the user to start the game
    elif keys[pygame.K_KP_ENTER]:
        for squar in squares:
            squar.ready = True
        ready = True
    
    #clears the grid of all squares
    elif keys[pygame.K_BACKSPACE]:
        start = False
        ready = False
        squares = []
    
    #shows the map
    elif keys[pygame.K_TAB]:
        showMap = True
    
    elif keys[pygame.K_f]:      
        print("The game currently runs at: ", int(frames) ," frames per second.")
    #cleans the map from previous square positions
    
                                
    if showMap:
        map = []
        
        for i in range(25):
            map.append('0000000000000000000000000')    
        
    #redrawing before removing the squares so that the computer has to time to process
    #the next generation.   
    redrawGameWindow()
    
    
    if ready:
        #the reproduction cycle: checks all of the squares
        for squar in squares:
            
            #finding the "left" and "up" sides of the box containing all of the living cells
            if squar.xPos < xSquareMin:
                xSquareMin = squar.xPos
            
            if squar.yPos < ySquareMin:
                ySquareMin = squar.yPos
            
            #finding the "right" and "down" sides of the box containing all of the living cells
            if squar.xPos > xSquareMax:
                xSquareMax = squar.xPos
            
            if squar.yPos > ySquareMax:
                ySquareMax = squar.yPos
        
        for i in range((ySquareMin-20)//10,(ySquareMax+40)//10):
            xPos = xSquareMin-20
            for j in range((xSquareMin-20)//10,(xSquareMax+40)//10):
                #checks the middle of each square to avoid ambiguities
                yPos = i*10
                xPos += 10
                
                #if the color of the square isn't red
                if ( WinBounds - 1 > xPos > 0 and WinBounds-1 > yPos > 0):
                    if win.get_at((xPos,yPos))[0] != 255:
                        
                        #check the adjacent squares
                        flag = checkAdjacentSquares(win, xPos - xPos%20, yPos - yPos%20) + 1
                        
                        #the reproducing condition
                        if flag == 3:
                            #creating the new reproduced squares
                            squares.append(square(xPos - xPos%20, yPos - yPos%20,1,(255,0,0))) 
        
        #Needs to cycle eight times to check every square in the 3x3 grid (except the square in the middle)
        for i in range(8):
            for squar in squares:
                if squar.ready:
                    squar.flag = checkAdjacentSquares(win,squar.xPos,squar.yPos)
                    
                    #the dying conditions
                    if squar.flag < 2 :
                        squares.remove(squar)
                        
                    elif squar.flag > 3 :
                        squares.remove(squar)
                        
    
    if showMap:
        updateMap()
        
        #if there actually is a map
        if len(map) > 0:
            #shows the map
            for i in map:
                print(i)
            print("")
    
    #if not enough squares the Game restarts
    if len(squares) == 0:
        start = False
        ready = False
    
    showMap = False
    frames = (1/(time.time()-starty))

pygame.quit()








#P.S:
#for crazy maze generation:
#   count must be 0
#   the reproduction flag must be 3
#   the overpopulation flag must be 4
#   ln.62 must recognise the alive cells only
