'''
Created on Oct 23, 2013

@author: Mike
'''
from Parser.CustomTypes import *
import sys
import pygame



class Renderer(object):
    MAX_WIDTH = 1200
    MAX_HEIGHT = 700
    HOUSE_SPACER = 10
    BLOCK_X_SPACER = 20 #Space between the edge of the picture and the left and right sides of a block, or between blocks
    BLOCK_Y_SPACER = 20 #Space between the edge of the picture and the top or botom of a block, or between blocks
    BLOCK_HEIGHT = 100
    
    BACKGROUND_COLOUR = (169,167,146)
    GREEN_BLOCK_COLOUR = (141,153,109)
    
    screen = {}
    
    packages = []
    packageCount = 0
    
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
    currentHouseTopLeft = (0,0)
    
    def _init_(self, packages):
        self.packages = packages

        
    def setPackages(self, packages):
        self.packages = packages

        
    '''
    Call this method to generate the output image
    '''
    def renderNeighbourhood(self):
        self.rowWidth = (self.MAX_WIDTH / 2) - (1.5 * self.BLOCK_X_SPACER)
        self.remainingRowWidth = self.rowWidth
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
        '''
        self.buildPackage(self.packages[0])
        '''
        return None

    def buildPackage(self, package):
        #Packages are implicitly represented in the output as blocks which are close together
        for module in package.modules:
            self.buildBlock(module)
        return None


    def buildBlock (self, module):
        #Modules are explicitly represented in the output as blocks (of 'grass') which surround the houses(classes) of that module
        blockRects = self.calculateBlockDimensions(module) #a list of tuples representing the rect dimensions for a single block

        i = 0
        colours = [(141,153,109), (0,0,255), (0,0,0)]
        for br in blockRects:
            x = br[0]
            y = br[1]
            c = br[2]
            
            colour = colours[i]
            
            if (x > self.remainingRowWidth): #Go to next row
                self.currentY = self.currentY + self.BLOCK_HEIGHT + self.BLOCK_Y_SPACER
                if (self.currentSide == 'L'):
                    self.currentX = self.BLOCK_X_SPACER
                    self.remainingRowWidth = self.rowWidth
            
            if (c == 1): #block fits perfectly in row
                blockTopLeft = (self.currentX, self.currentY)
                block = Block(blockTopLeft, x, y, colour)
                self.blocks.append(block)
                self.currentY = self.currentY + self.BLOCK_HEIGHT + self.BLOCK_Y_SPACER #Go to next row
                self.remainingRowWidth = self.rowWidth
                
            if (c == 0):
                if self.remainingRowWidth != self.rowWidth:
                    self.currentX = self.currentX + self.BLOCK_X_SPACER
                    
                blockTopLeft = (self.currentX, self.currentY)
                self.currentX = self.currentX + x
                block = Block(blockTopLeft, x, y, colour)
                self.blocks.append(block)
                self.remainingRowWidth = self.remainingRowWidth - x
                
            #FOR TESTING - REMOVE LATER
            
            print '***************'
            print block.getTopLeft()
            print block.getWidth()
            print block.getLength()
            prnt1 = ('row width', self.rowWidth)
            print prnt1
            prnt2 = ('remaining row width', self.remainingRowWidth)
            print prnt2
            print '****   ********'
            i = i + 1
        return None
    '''
    Return a list of tuples (x,y, c) which are the width, height of the rectangles needed to represent a block, and c
    is 1 if the rectangle occupies a complete row, and 0 if it occupies a partial row
    '''
    def calculateBlockDimensions(self, module):
        dimensions = []
        classes = module.getClasses()
        #Determine the width needed to represent a block
        totalWidth = 0
        for c in classes:
            totalWidth = totalWidth + self.HOUSE_SPACER
            width = c.getWidth()
            totalWidth = totalWidth + width
        
        lastHouseWidth = width
        
        halfScreen = (self.MAX_WIDTH / 2) - (1.5 * self.BLOCK_X_SPACER)
        
        tempTotalWidth = totalWidth
        
        while (tempTotalWidth > halfScreen):
            tempTotalWidth = tempTotalWidth - halfScreen
            rect = (halfScreen, self.BLOCK_HEIGHT, 1)
            dimensions.append(rect)
        
        if (tempTotalWidth != 0):
            if (tempTotalWidth >= lastHouseWidth):
                rect = (tempTotalWidth, self.BLOCK_HEIGHT, 0)
            else:
                rect = (lastHouseWidth, self.BLOCK_HEIGHT, 0)
            dimensions.append(rect)
        return dimensions

        
    def buildHouse(self, theClass):
        #TDOO Implement
        return None
    
    def buildWindow(self, method):
        #TODO Implement
        return None
    
    def initDrawing(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAX_WIDTH, self.MAX_HEIGHT))
        self.screen.fill(self.BACKGROUND_COLOUR)
        return None
    
    def drawBlocks(self):
        for block in self.blocks:
            self.drawBlock(block)
        return None
    
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


#FOR TESTTING
def main():
    
    
    #make some packages
    package1 = Package('P1')
    package2 = Package('P2')
    package3 = Package('P3')
    
    #make some classes:
    class1 = Class('Class1', 10, 60, 8)
    class2 = Class('Class2', 10, 120, 9)
    class3 = Class('Class3', 10, 45, 7)
    class4 = Class('Class4', 10, 75, 8)
    class5 = Class('Class5', 10, 90, 4)
    class6 = Class('Class6', 10, 60, 6)
    class7 = Class('Class7', 10, 70, 5)
    
    #No methods in this iteration
    
    #Package1:
    module1 = Module('Module1')
    module2 = Module('Module2')

    module1.addClass(class5)
    module1.addClass(class3)
    module2.addClass(class1)
    module2.addClass(class4)
    module2.addClass(class2)
    
    package1.addModule(module1)
    package1.addModule(module2)
    
    #Package2:
    module3 = Module('Module3')
    module4 = Module('Module4')
    module5 = Module('Module5')
    
    module3.addClass(class2)
    module3.addClass(class7)
    module4.addClass(class5)
    module5.addClass(class1)
    module5.addClass(class4)
    module5.addClass(class6)
    
    package2.addModule(module3)
    package2.addModule(module4)
    package2.addModule(module5)
    
    #Package3:
    module6 = Module('Module6')
    
    module6.addClass(class3)
    module6.addClass(class7)
    module6.addClass(class2)
    module6.addClass(class5)
    module6.addClass(class1)
    module6.addClass(class4)
    module6.addClass(class6)
    
    package3.addModule(module6)


    packagesOne = []
    packagesOne.append(package1)
    packagesOne.append(package2)
    packagesOne.append(package3)
    
    renderer = Renderer()
    renderer.setPackages(packagesOne)
    
    renderer.renderNeighbourhood()
    return None
                
        
        
if __name__ == "__main__":
        main()
  
        
        

