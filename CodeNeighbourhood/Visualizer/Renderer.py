'''
Created on Oct 23, 2013

@author: Mike
'''
from CustomTypes import *
import sys
import pygame

class Renderer(object):
    MAX_WIDTH = 1200
    MAX_HEIGHT = 700
    HOUSE_X_SPACER = 10
    HOUSE_Y_SPACER = 10
    BLOCK_X_SPACER = 20 #Space between the edge of the picture and the left and right sides of a block, or between blocks
    BLOCK_Y_SPACER = 20 #Space between the edge of the picture and the top or botom of a block, or between blocks
    BLOCK_HEIGHT = 100
    MIN_BLOCK_WIDTH = 100
    WIDTH_MULTIPLIER = 10 #For first iteration only - once "width" becomes more accurate, not needed
    
    BACKGROUND_COLOUR = (169,167,146)
    GREEN_BLOCK_COLOUR = (141,153,109)
    RED_HOUSE_COLOUR = (256,0,0)
    
    screen = {}
    packages = []
    houses = []
    windows = []
    tents = []
    powerlines = []
    clotheslines = []
    fountain = {}
    blocks = []
    
    currentX = BLOCK_X_SPACER
    currentY = BLOCK_Y_SPACER
    currentSide = 'L'  #'L' or 'R'
    rowWidth = 0
    remainingRowWidth = 0
    rightSideRowStart = 0
    totalRowHeight = 0
    remainingRowHeight = 0
    
    def __init__(self, packages):
        self.packages = packages
        
    '''
    Call this method to generate the output image
    '''
    def renderNeighbourhood(self):
        #self.rowWidth = (self.MAX_WIDTH / 2) - (1.5 * self.BLOCK_X_SPACER) #- Uncomment to change to half-screen spacing
        self.rowWidth = self.MAX_WIDTH - 2 * self.BLOCK_X_SPACER
        self.remainingRowWidth = self.rowWidth
        self.rowHeight = (self.MAX_HEIGHT - 2 * self.BLOCK_Y_SPACER)
        self.remainingRowHeight = self.rowHeight
        self.rightSideRowStart = self.BLOCK_X_SPACER * 2 + self.rowWidth
        self.buildNeighbourhood()
        self.initDrawing()
        #draw individual elements here
        self.drawBlocks()
        
        #finalize drawing
        pygame.display.update()
        control = 1
        while control:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
        
        return None
    
    def buildNeighbourhood(self):
        
        for package in self.packages:
            self.buildPackage(package)
        return None

    def buildPackage(self, package):
        #Packages are implicitly represented in the output as blocks which are close together
        for module in package.modules:
            self.buildBlock(module)
        return None

    def buildBlock (self, module):
        #Modules are explicitly represented in the output as blocks (of 'grass') which surround the houses(classes) of that module
        blockRects = self.calculateBlockDimensions(module) #a list of tuples representing the rect dimensions for a single block
        colour = self.GREEN_BLOCK_COLOUR #change later to represent module score
        i = 0
        length = len(blockRects)
        while i < length:
     
            x = blockRects[i][0]
            y = blockRects[i][1]
            c = blockRects[i][2]
            
            topLeft = self.blockCalculatePosition(x, y)
            block = Block(topLeft, x, y, colour)
            self.blocks.append(block)
            
            if (c == 1 and i != length - 1 and blockRects[i+1][2] != 1): #the block spans more than 1 row and the current rect is the last complete row
                width = blockRects[i+1][0]
                miniTopLeft = (topLeft[0], topLeft[1] + self.BLOCK_HEIGHT)
                miniBlock = Block(miniTopLeft, width, self.BLOCK_Y_SPACER, colour)
                self.blocks.append(miniBlock)
                print width
            
            i = i + 1
            #FOR TESTING - REMOVE LATER

        return None
    '''
    Return a list of tuples (x,y,c) which are the width, height of the rectangles needed to represent a block, and c
    is 1 if the rectangle occupies a complete row, and 0 if it occupies a partial row
    '''
    def calculateBlockDimensions(self, module):
        dimensions = []
        classes = module.getClasses()
        #Determine the width needed to represent a block
        totalWidth = 0
        width = 0
        for c in classes:
            totalWidth = totalWidth + self.HOUSE_X_SPACER

            width = int(c.getWidth())
            totalWidth = totalWidth + width
        
        totalWidth = totalWidth * self.WIDTH_MULTIPLIER
            
        lastHouseWidth = width
        halfScreen = self.rowWidth
        tempTotalWidth = totalWidth
        
        #create n number of full row rects
    
        while (tempTotalWidth > halfScreen):
            tempTotalWidth = tempTotalWidth - halfScreen
            rect = (halfScreen, self.BLOCK_HEIGHT, 1)
            dimensions.append(rect)
            
        #create the last rect
        
        if (tempTotalWidth != 0):
            if (tempTotalWidth >= lastHouseWidth):
                rect = (tempTotalWidth, self.BLOCK_HEIGHT, 0)
            elif(lastHouseWidth > self.MIN_BLOCK_WIDTH):
                rect = (lastHouseWidth, self.BLOCK_HEIGHT, 0)
            else:
                rect = (self.MIN_BLOCK_WIDTH, self.BLOCK_HEIGHT, 0)
            dimensions.append(rect)
        return dimensions
    

    def buildHouse(self, theClass):
        #TDOO Implement
        return None
    
    def buildWindow(self, method):
        #TODO Implement
        return None
    
    '''
    Initialize the output window
    '''
    def initDrawing(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAX_WIDTH, self.MAX_HEIGHT))
        self.screen.fill(self.BACKGROUND_COLOUR)
        return None
    
    '''
    Render the Blocks
    '''
    def drawBlocks(self):
        for block in self.blocks:
            self.drawBlock(block)
        return None
    '''
    Render a Block
    '''
    def drawBlock(self, block):
        topLeft = block.getTopLeft()
        left = topLeft[0]
        top = topLeft[1]
        length = block.getLength()
        width = block.getWidth()
        colour = block.getColour()
        
        rect = (left, top, width, length)
        
        pygame.draw.rect(self.screen, colour, rect, 0)
        
        return None     
    
    def drawHouses(self):
        for house in self.houses:
            self.drawHouse(house)
        return None
    
    def drawHouse(self, house):
        #TODO Implement
        return None
    
    def drawWindow(self, window):
        #TODO Implement
        return None
    
    def drawFountain(self, fountain):
        #TODO Implement
        return None     

    def drawClothesline(self, clothesline):
        #TODO Implement
        return None
    
    def drawPowerline(self, powerline):
        #TODO Implement
        return None
    
    def drawTent(self, tent):
        #TODO Implement
        return None  
    '''        
    Find the next available place for a block given the width and height, and update
    currentX, currentY, currentSide accordingly
    returns (x,y) as the topLeft coords of the block
    '''
    def blockCalculatePosition(self, width, height):
        topLeft = (0,0)
        spaceForNewRow = 0
        if (self.remainingRowHeight >= (1 * self.BLOCK_Y_SPACER) + 2 * self.BLOCK_HEIGHT):
            spaceForNewRow = 1   
        spaceOnCurrentRow = 0
        if (self.remainingRowWidth >= width):
            spaceOnCurrentRow = 1
        
        if (spaceOnCurrentRow == 1): #if there's space on the current row:
            self.currentX = self.currentX
            topLeft = (self.currentX, self.currentY);
            self.blockUpdateHorizontalPosition(width)
            return topLeft

        else: #go to a new row
            self.remainingRowWidth = self.rowWidth
            if (spaceForNewRow == 1):
                #go to start of a new row on the same side
                if self.currentSide == 'L':
                    self.currentX = self.BLOCK_X_SPACER
                    self.blockUpdateVerticalPosition(height)
                elif self.currentSide == 'R':
                    self.currentX = self.rightSideRowStart
                    self.blockUpdateVerticalPosition(height)
                topLeft = (self.currentX, self.currentY)
                self.blockUpdateHorizontalPosition(width)
                return topLeft
                
            else:  #go to other side
                if self.currentSide == 'L':
                    self.currentX = self.rightSideRowStart
                    self.currentY = self.BLOCK_Y_SPACER
                    self.remainingRowHeight = self.rowHeight
                    self.currentSide = 'R'
                    topLeft = (self.currentX, self.currentY)
                    self.blockUpdateHorizontalPosition(width)
                    return topLeft
    '''
    update currentX and remainingRowWidth  after the addition of a new block
    '''
    def blockUpdateHorizontalPosition(self, width):
        self.currentX = self.currentX + width + self.BLOCK_X_SPACER
        self.remainingRowWidth = self.remainingRowWidth - width - self.BLOCK_X_SPACER
        return None
    '''
    update currentY and remainingRowHeight after the additoon of a new block in a new row
    '''
    def blockUpdateVerticalPosition(self, height):
        self.currentY = self.currentY + height + self.BLOCK_Y_SPACER
        self.remainingRowHeight = self.remainingRowHeight - height - self.BLOCK_Y_SPACER
        return None
    
class House(object):
    name = ''
    length = 0
    width = 0
    topLeft = (0,0)
    condition = 0
    
    def _init_(self, name, length, width, topLeft, condition):
        self.name = name
        self.length = length
        self.width = width
        self.topLeft = topLeft
        self.condition = condition

class Window(object):
    height = 0
    width = 0
    colour = (0,0,0)
    topLeft = (0,0)
    
    def __init__(self, height, width, colour, topLeft):
        self.height = height
        self.width = width
        self.colour = colour
        self.topLeft = topLeft
        
class Tent(object):
    topLeft = (0,0)
    
    def __init__(self, topLeft):
        self.topLeft = topLeft
        
class Powerline(object):
    start = (0,0)
    finish = (0,0)
    
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish

class Clothesline(object):
    start = (0,0)
    finish = (0,0)
    
    def _init_(self, start, finish):
        self.start = start
        self.finish = finish

class Fountain(object):
    topLeft = (0,0)
    
    def __init__(self, topLeft):
        self.topLeft = topLeft
        
class Block(object):
    topLeft = (0,0)
    length = 0
    width = 0
    colour = (0,0,0)
    
    def __init__(self, topLeft, width, length, colour):
        self.topLeft = topLeft
        self.length = length
        self.width = width
        self.colour = colour
        
    def getTopLeft(self):
        return self.topLeft
    
    def getLength(self):
        return self.length
    
    def getWidth(self):
        return self.width
    
    def getColour(self):
        return self.colour
