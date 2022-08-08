import random
import pygame
import sys

"""logic for maze creation (PRIM'S ALGORITHM)

The depth-first search algorithm of maze generation is frequently implemented using backtracking. This can be described with a following recursive routine:

Choose the initial cell, mark it as visited and push it to the stack
While the stack is not empty
Pop a cell from the stack and make it a current cell
If the current cell has any neighbours which have not been visited
Push the current cell to the stack
Choose one of the unvisited neighbours
Remove the wall between the current cell and the chosen cell
Mark the chosen cell as visited and push it to the stack

"""

# constants

SCREEN_HEIGHT = 1024
SCREEN_WIDTH = 1024


GRID_HEIGHT = int(input("give a number from 4 to 512, for the height, (preferably keep width the same)")) # coordinates start from 0, so length is technically 4
GRID_WIDTH = int(input("give a number from 4 to 512, for the width"))

CUBE_LENGTH = SCREEN_HEIGHT//GRID_HEIGHT

LINE_WIDTH = CUBE_LENGTH//2

FONTSIZE = SCREEN_HEIGHT//16

CENTER_X = SCREEN_WIDTH//2 
CENTER_Y = SCREEN_HEIGHT//2 

#-->Game Booleans
game_start = True
menu_start = True

#--> initialization

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("MazeGenerator")

#-->Color Values

BCG_COLOR = (0,0,0)
TEXT_COLOR = (0, 255, 65)
LINE_COLOR = (0, 255, 65)
HIGHLIGHT_COLOR = (0, 59, 0)

RGB = [( 0, 0, 255), (0,255,0), (255, 0, 0)]

BODY_COLOR = (0, 255, 65)

#-->Text Assets


#------->fonts

# Corbel, Times New Roman, berlinsanafb

HEADER_FONT = pygame.font.SysFont("berlinsanafb", FONTSIZE)#heading font
NORMAL_FONT = pygame.font.SysFont("berlinsanafb", FONTSIZE)#font for everything else


#------->text class

class Text(): # class that encompasses anything with text, i.e a button or header or score
	def __init__(self, x, y, text, color, font):
		self.color = color
		self.font = font
		self.text = text
		self.textRender = font.render(text, True, color)
		self.rect = self.textRender.get_rect(center=(x,y))


	def drawText(self, event):
		mouseX, mouseY = pygame.mouse.get_pos() # coords of the mouse
		
		if self.rect.collidepoint((mouseX, mouseY)): # to see if the cursor is over the button
			self.textRender = self.font.render(self.text, True, HIGHLIGHT_COLOR)
			if event.type == 1025 and event.button == 1: # if it is a mouse button down, and the button is a left click
				return True

		else:
			self.textRender = self.font.render(self.text, True, self.color)
		
		screen.blit(self.textRender, self.rect)

#-------->text instances

title = Text(CENTER_X, CENTER_Y - (SCREEN_HEIGHT//4), "Maze", TEXT_COLOR, HEADER_FONT)
exitButton = Text(CENTER_X , CENTER_Y, "Exit", TEXT_COLOR, NORMAL_FONT)
newgameButton = Text(CENTER_X , CENTER_Y - (SCREEN_HEIGHT//8), "New Maze", TEXT_COLOR, NORMAL_FONT)

#--> Board Classes

class Cell():
	def __init__(self, x, y): # here, x and y arent positions on screen, but the coordinate on the grid, which we need to translate to screen coordinates as well...
		self.x = x
		self.y = y

		self.topLeft = (x*CUBE_LENGTH, y*CUBE_LENGTH)
		self.bottomRight = (x*CUBE_LENGTH + CUBE_LENGTH, y*CUBE_LENGTH + CUBE_LENGTH)
		self.topRight = (x*CUBE_LENGTH + CUBE_LENGTH, y*CUBE_LENGTH)
		self.bottomLeft = (x*CUBE_LENGTH, y*CUBE_LENGTH + CUBE_LENGTH)

		self.wallCode = {"top": True,"bottom":True,"left": True , "right": True} # represents the walls of the cell, i.e the top, left, bottom, right walls
		self.visitedByConstructor = False
		#self.visitedByPlayer = False # bool that states whether a cell has been visited by the player or not
		self.LINE_COLOR = (0, 255, 65)


	@classmethod
	def createCell(cls, x, y):
		return cls(x,y)


class Maze():
	def __init__(self, width, height):
		self.board = [[Cell.createCell(i, j) for i in range(width)] for j in range(height)]
		self.mazeBuilt = False # bool that says if the cell has been built or not
		self.currentCell = (0,0) # the (x,y) coords of the current cell
		self.visitedCellsCount = 1 # the total cells visited
		self.cellPathStack = [] # a stack that contains the current path of the pattern, needed for being able to backtrack

	def createMaze(self):# creates the structure of the maze
		j, i = random.randint(0,GRID_HEIGHT-1), random.randint(0, GRID_WIDTH-1)# chooses a cell coord on the board
		
		if not self.mazeBuilt:

			currentCell = self.board[j][i]

			currentCell.visitedByConstructor = True
			
			self.cellPathStack.append((i, j))

			while self.visitedCellsCount < (GRID_WIDTH*GRID_HEIGHT): # while cells visited is less than total number of cells
			
				possibleMoves = [] # returns the directions in the cell that still have walls

				for i in currentCell.wallCode.keys():
					if currentCell.wallCode[i]: # if there is a wall in this direction
						if i == "top" and currentCell.y - 1 >= 0 and not self.board[currentCell.y-1][currentCell.x].visitedByConstructor: # if the wall is the top wall, and the cell above it hasnt been visited and is on the board
							possibleMoves.append(i) 
						if i == "bottom" and currentCell.y + 1 < GRID_HEIGHT and not self.board[currentCell.y+1][currentCell.x].visitedByConstructor:
							possibleMoves.append(i)
						if i == "right" and currentCell.x + 1 < GRID_WIDTH and not self.board[currentCell.y][currentCell.x+1].visitedByConstructor:
							possibleMoves.append(i)  
						if i == "left" and currentCell.x - 1 >= 0 and not self.board[currentCell.y][currentCell.x-1].visitedByConstructor:
							possibleMoves.append(i) 
				
				if len(possibleMoves) != 0:# if there are any walls to break
					
					direction = random.choice(possibleMoves)
					self.visitedCellsCount += 1
					
					currentCell.wallCode[direction] = False

					if direction == "top" and not self.board[currentCell.y-1][currentCell.x].visitedByConstructor:
						
						self.cellPathStack.append( (currentCell.x, currentCell.y - 1) )
						currentCell = self.board[currentCell.y - 1][currentCell.x]
						currentCell.wallCode["bottom"] = False
					
					if direction == "bottom":	
						self.cellPathStack.append( (currentCell.x, currentCell.y + 1) )
						currentCell = self.board[currentCell.y + 1][currentCell.x]
						currentCell.wallCode["top"] = False
					
					if direction == "right":
						self.cellPathStack.append( (currentCell.x + 1, currentCell.y ) )
						currentCell = self.board[currentCell.y][currentCell.x + 1]
						currentCell.wallCode["left"] = False
					
					if direction == "left":
						self.cellPathStack.append( (currentCell.x - 1, currentCell.y) )
						currentCell = self.board[currentCell.y][currentCell.x - 1]
						currentCell.wallCode["right"] = False

					currentCell.visitedByConstructor = True

				if len(possibleMoves) == 0: # there are no walls to break for a particular cell, meaning backtracking is necessary
					self.cellPathStack.pop()
					currentCell = self.board[self.cellPathStack[-1][1]][self.cellPathStack[-1][0]]

		self.mazeBuilt = True
	
	def drawMaze(self): # draws the maze onto the screen
		screen.fill(BCG_COLOR)

		for column in self.board:
			for cell in column:
				if cell.wallCode["top"]:
					pygame.draw.line(screen, cell.LINE_COLOR, cell.topRight, cell.topLeft, width = LINE_WIDTH)
				if cell.wallCode["right"]:
					pygame.draw.line(screen, cell.LINE_COLOR, cell.topRight, cell.bottomRight, width = LINE_WIDTH)
				if cell.wallCode["bottom"]:
					pygame.draw.line(screen, cell.LINE_COLOR, cell.bottomRight, cell.bottomLeft, width = LINE_WIDTH)
				if cell.wallCode["left"]:
					pygame.draw.line(screen, cell.LINE_COLOR, cell.bottomLeft, cell.topLeft, width = LINE_WIDTH)

		pygame.display.update()


#--> game objects 

gameBoard = Maze(GRID_WIDTH, GRID_HEIGHT)


#--> main game

def menu():
	global menu_start, game_start
	while menu_start:
		screen.fill(BCG_COLOR)
		for event in pygame.event.get():			
			
			title.drawText(event)
			if exitButton.drawText(event):
				menu_start = False
				game_start = False
				return False
			
			if newgameButton.drawText(event):
				game_start = True
				menu_start = False
				return True
			
			if event.type == pygame.QUIT:
				menu_start = False
				game_start = False
				return False
		

			pygame.display.update()

def game():
	global game_start, menu_start
	
	gameBoard.createMaze()
	while game_start:

		
		for event in pygame.event.get():			
			
			if event.type == pygame.QUIT:
				menu_start = False
				game_start = False
				return False

		gameBoard.drawMaze()


def main():
	running = True

	while running:	
		if menu_start:
			running = menu()
		if game_start:
			running = game()
	
	pygame.quit()
	sys.exit()

main()