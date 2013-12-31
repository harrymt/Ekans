import pygame, random, sys
from pygame.locals import *

# The direction of Ekans
DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3

# ----------------------------------------------------------------
# Collide Function:
# Check to see if 2 sets of coordinates overlap
def collide(x1, x2, y1, y2):
    if x1 == x2 and y1 == y2:
        return True
    else:
        return False

# ----------------------------------------------------------------
# Random position function
# Generates a random position for the gem
# Forced to a multiple of 25 to keep it alligned with grid
# If newPos overlaps a current Ekans segment, generates another
def randomGem():
    while True:
        valid = True
        newPos = ((random.randint(2,19)) * 25, (random.randint(2,19)) * 25)
   
        for i in xrange(len(xs) - 1):
            if collide(newPos[0], xs[i], newPos[1], ys[i]): valid = False

        if valid == True: return newPos

# ----------------------------------------------------------------

# Initilize the game engine
pygame.init()

# Create the screen in a window with the title 'Ekans'
# 600x600 pixels
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Ekans')

# Initialize default game speed
gameSpeed = 1

# Create objects used for title, menu and game stats
tFont = pygame.font.SysFont('Comic Sans MS', 80)
title = tFont.render('Ekans', 1, (255, 0, 255))

iFont = pygame.font.SysFont('Comic Sans MS', 30)
mFont = pygame.font.SysFont('Comic Sans MS', 60)
mInfo = iFont.render('Choose an option and press return:', 1, (0, 0, 0))
mStart = mFont.render('Start game', 1, (0, 0, 0))
mSpeedLabel = mFont.render('Speed:', 1, (0, 0, 0))
mSpeed = mFont.render(str(gameSpeed), 1, (0, 0, 0))
mQuit = mFont.render('Quit', 1, (0, 0, 0))

selected = pygame.Surface((600, 50))
selected.fill((255, 0, 0))

sEndTitle = mFont.render('Game Over!', 1, (0, 0, 0))
sInfo = mFont.render('Press return', 1, (0, 0, 0))

# Create the game area
# The area where Ekans is allowed
area = pygame.Surface((500, 500))
area.fill((0, 255, 0))

# Creates the 'gem'
# This is a 25x25 square, which spawns randomly on the screen
gemimage = pygame.Surface((25, 25))
gemimage.fill((0, 0, 255))

# Creates the 'supergem'
# This is a 25x25 square, which spawns randomly on the screen
# Spawns at the same time as every tenth gem
# Dissapears after 40 shifts and worth the normal points x 3
sgemimage = pygame.Surface((25,25))
sgemimage.fill((255, 0, 0))

# Creates the 'Ekans' segment
# This is a 25x25 square repeated in series
ekansimage = pygame.Surface((25, 25))
ekansimage.fill((255, 0, 255))

# Creates the score counter
# This is a string displaying the current score
sFont = pygame.font.SysFont('Comic Sans MS', 60)

# Creates clock used for setting game speed
clock = pygame.time.Clock()

while True:

    # Intialize variables used for menu
    startGame = False
    selectPos = 200

    # Run menu until user starts the game
    while startGame == False:

        # Draw menu items
        screen.fill((0, 255, 0))
        screen.blit(selected, (0, selectPos))
        screen.blit(title, (100, 50))
        screen.blit(mInfo, (100, 150))
        screen.blit(mStart, (100, 200))
        screen.blit(mSpeedLabel, (100, 250))
        screen.blit(mSpeed, (250, 250))
        screen.blit(mQuit, (100, 300))

        # Update the screen with newly drawn objects
        pygame.display.update()

        # Wait for user input and read it
        ev = pygame.event.wait()

        # If the OS asks the program to quit
        # e.g. if the user clicked 'x'
        if ev.type == pygame.QUIT: pygame.quit()

        # If the user presses a key
        elif ev.type == KEYDOWN:

            # If up or down pressed, move selection bar
            if ev.key == K_UP and selectPos > 200: selectPos -= 50
            elif ev.key == K_DOWN and selectPos < 300: selectPos += 50

            # If the user has chosen a menu option
            elif ev.key == K_RETURN:
                if selectPos == 200:
                    startGame = True

                # Change the game speed on enter press
                # Ranged from 1 to 3
                # If currently 3, on enter go back to 1
                elif selectPos == 250:
                    gameSpeed -= 1
                    gameSpeed = (gameSpeed + 1) % 3
                    gameSpeed += 1

                    mSpeed = mFont.render(str(gameSpeed), 1, (0, 0, 0))

                elif selectPos == 300: pygame.quit()

    # Set initial direction to DOWN
    direction = DOWN

    # Represents x's and y's of each block of Ekans
    # xs[0],ys[0] == head position
    xs = [300, 300, 300, 300, 300]
    ys = [300, 275, 250, 225, 200]

    # The starting position of the gem
    gempos = randomGem()

    # Initialize score and gem variables
    score = 0
    cScore = sFont.render('Score: ' + str(score), 1, (0, 0, 0))
    gCount = 0
    sGCount = 0
    sGemActive = False

    # START OF GAME LOOP ---------------------------------------------
    while True:
        # Holds execution for specified time, tick(n) -> 1/n seconds
        # tick(n) also means run GAME LOOP n times per second -> nfps
        clock.tick(gameSpeed * 5)

        if sGemActive == True:
            if sGemTime == 0: sGemActive = False

        # For every event that has happened since last check
        for ev in pygame.event.get():

            # If the OS asks the program to quit
            # e.g. if the user clicked 'x'
            if ev.type == pygame.QUIT: pygame.quit()

            # Ekans moves in the direction the user presses
            elif ev.type == KEYDOWN:
                
                # If a direction key pressed is 
                # (NOT the opposite direction Ekans) 
                # then change to corresponding direction
                if ev.key == K_UP and direction != DOWN: direction = UP
                elif ev.key == K_DOWN and direction != UP: direction = DOWN
                elif ev.key == K_LEFT and direction != RIGHT: direction = LEFT
                elif ev.key == K_RIGHT and direction != LEFT: direction = RIGHT

                # Only perform the first direction key press for this cycle
                break

        # If Ekans collides with itself, end game
        i = len(xs)-1
        collision = False    
        while i >= 2:
            if collide(xs[0], xs[i], ys[0], ys[i]): collision = True
            i -= 1
        if collision == True: break

        # If Ekans picks up a super gem
        if sGemActive == True:

            sGemTime -= 1

            if collide(xs[0], sgempos[0], ys[0], sgempos[1]):

                # Increment score and super gem count
                score += gameSpeed * 3
                cScore = sFont.render('Score: ' + str(score), 1, (0, 0, 0))
                sGCount += 1

                sGemActive = False

        # If Ekans picks up a gem
        if collide(xs[0], gempos[0], ys[0], gempos[1]):

            # Add another segment to Ekans
            xs.append(0)
            ys.append(0)

            # Increment score and gem count
            score += gameSpeed
            cScore = sFont.render('Score: ' + str(score), 1, (0, 0, 0))
            gCount += 1

            # Set another random position for next gem
            gempos = randomGem()

            # For every 5 gems...
            if gCount % 5 == 0:

                # Get a position that does not overlap a gem
                while True:
                    sgempos = randomGem()
                    if sgempos != gempos: break

                sGemActive = True
                sGemTime = 50

        # If Ekans collides with the edge, end game
        if xs[0] < 50 or xs[0] == 550 or ys[0] < 50 or ys[0] == 550: break

        # i is the index of the end of the array
        i = len(xs)-1

        # Shifts the tail of the array
        # Works backwards through the array making each one the one in front
        # until index 1    
        while i >= 1:
            xs[i] = xs[i-1]
            ys[i] = ys[i-1]
            i -= 1

        # Changes the head position depending on the current direction  
        if direction == DOWN: ys[0] += 25
        elif direction == RIGHT: xs[0] += 25
        elif direction == UP: ys[0] -= 25
        elif direction == LEFT: xs[0] -= 25
        
        # Wipes the screen
        screen.fill((255, 255, 255))
        
        # Draws game area
        screen.blit(area, (50, 50))

        # Draw the gem onto the screen
        screen.blit(gemimage, gempos)

        # If super gem is active...
        if sGemActive == True:

            # Draw the super gem onto the screen
            screen.blit(sgemimage, sgempos)

        # Redraws Ekans with updated positions
        for i in range(0, len(xs)): screen.blit(ekansimage, (xs[i], ys[i]))

        # Draw score
        screen.blit(cScore, (50, 0))

        # Update the screen with newly drawn objects
        pygame.display.update()

    # END OF GAME LOOP ------------------------------------------

    # Create text for stats
    sGems = mFont.render('Gems: ' + str(gCount), 1, (0, 0, 0))
    sSuperGems = mFont.render('Supers: ' + str(sGCount), 1, (0, 0, 0))

    # Create the game area
    # The area where Ekans is allowed
    statsArea = pygame.Surface((300, 300))
    statsArea.fill((255, 255, 255))

    # Draw stats area and text
    screen.blit(statsArea, (150, 150))
    screen.blit(sEndTitle, (160, 160))
    screen.blit(cScore, (160, 210))
    screen.blit(sGems, (160, 260))
    screen.blit(sSuperGems, (160, 310))
    screen.blit(sInfo, (160, 400))

    # Update screen with newly drawn objects
    pygame.display.update()

    # Keep taking user input...
    while True:
        ev = pygame.event.wait()

        # ...until either the use closes the window...
        if ev.type == pygame.QUIT: pygame.quit()

        # ...Or the user presses return
        # If so return to menu
        if ev.type == KEYDOWN:
            if ev.key == K_RETURN: break