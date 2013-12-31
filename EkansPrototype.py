import pygame, random, sys
from pygame.locals import *

# Initilize the game engine
pygame.init()

# Create the screen on a 500x500 grid with the title 'Ekans'
# 500x500 pixels
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Ekans')

# Represents x's and y's of each block of Ekans
# segX[0],segY[0] == head position
segX = [250, 250, 250, 250]
segY = [250, 225, 200, 175]

# Creates the 'Ekans' segment
# This is a 25x25 square repeated in series
# The initial positions of the first segments are in 'segX' and 'segY'
# This is actually drawn later
ekansImage = pygame.Surface((25, 25))
ekansImage.fill((255, 0, 255))

# The starting position of the gem
# Randomly generated numbers between or equal to 0 and 475
# forced to a multiple of 25 to keep it alligned with grid
gemPos = ((random.randint(0,19))*25,(random.randint(0,19))*25)

# Creates the 'gem'
# This is a 25x25 square, which spawns randomly on the screen
# The initial position 'gemPos' was created earlier
# This is actually drawn later
gemImage = pygame.Surface((25, 25))
gemImage.fill((0, 0, 255))

running = True
fps = pygame.time.Clock()

# START OF GAME LOOP ---------------------------------------------
while running == True:

	# Wipes the screen
	screen.fill((0, 255, 0))

	# Redraws Ekans with updated positions
	for count in range(0, len(segX)):
		screen.blit(ekansImage, (segX[count], segY[count]))

	# Draw the gem onto the screen
	screen.blit(gemImage, gemPos)

	# Update the screen with newly drawn objects
	pygame.display.update()

	# Holds execution for specified time, tick(10) -> 1/10 seconds
	# tick(10) also means run GAME LOOP 10 times per second -> 10fps
	fps.tick(5)

	# Shifts the tail of the array
	# Works backwards through the array making each one the one in front
	# until index 1 
	count = len(segX)-1
	while count > 0:
		segX[count] = segX[count-1]
		segY[count] = segY[count-1]
		count -= 1

	# Shifts head position
	segY[0] += 25
# RESTART GAME LOOP ------------------------------------------