'''
Created on Oct 23, 2013

@author: Mike
'''
from Analyzer.CustomTypes import *
import sys
import pygame
from random import randint

class Renderer(object):
    MAX_WIDTH = 1100
    MAX_HEIGHT = 800
    HOUSE_X_SPACER = 20
    HOUSE_Y_SPACER = 20
    BLOCK_X_SPACER = 20 #Space between the edge of the picture and the left and right sides of a block, or between blocks
    BLOCK_Y_SPACER = 40 #Space between the edge of the picture and the top or botom of a block, or between blocks
    BLOCK_HEIGHT = 100
    BLOCK_CORNER_RADIUS = 15
    MIN_BLOCK_WIDTH = 80
    NO_CLASS_BLOCK_WIDTH = 60
    HOUSE_MIN_HEIGHT = 40
    HOUSE_ROOF_HEIGHT = 20
    HOUSE_DOOR_HEIGHT = 20
    HOUSE_DOOR_WIDTH = 10
    
    WINDOW_X_SPACER = 4
    WINDOW_Y_SPACER = 5
    WINDOW_MIN_HEIGHT = 5
    WINDOW_MIN_WIDTH = 5
    WINDOW_WIDTH_MULTIPLIER = 20
    WINDOW_HEIGHT_MULTIPLIER = 2
    
    WINDOW_ROW_HEIGHT = 5
    
    TENT_WIDTH = 40
    TENT_HEIGHT = 20
    TENT_COLOUR = (228, 219, 137)
    TENT_X_SPACER = 30
    TENT_Y_SPACER = 50
    
    BACKGROUND_COLOUR = (169,167,146)
    PACKAGE_BLOCK_COLOURS = [ (68,131,7), (141,153,109),(87,158,18), (96,149,84), (141,173,109), (89,158,22)]
    RED_HOUSE_COLOUR = (255,0,0)
    HOUSE_COLOURS = [(0,174, 239), (255,255,255), (255, 242,0), (123, 114, 180), (255, 184, 107), (224, 133, 141), (121, 182, 176), (197, 232, 156)]
    HOUSE_DOOR_AND_ROOF_COLOUR = (115,99,87)

    
    screen = {}
    packages = []
    houses = []
    tents = []
    powerlines = []
    clotheslines = []
    fountain = {}
    blocks = []
    
    currentX = BLOCK_X_SPACER
    currentY = BLOCK_Y_SPACER * 2
    currentSide = 'L'  #'L' or 'R'
    rowWidth = 0
    remainingRowWidth = 0
    rightSideRowStart = 0
    totalRowHeight = 0
    remainingRowHeight = 0
    blockColourCounter = 0
    lastHouseColourIndex = 0
    blockCurrentX = 0
    blockCurrentY = 0
    windowCurrentX = 0
    windowCurrentY = 0
    windowRows = 0
    windowCurrentRow = 0
    windowTallestWindow = 0
    
    def __init__(self, packages):
        self.packages = packages
        
    '''
    Call this method to generate the output image
    '''
    def renderNeighbourhood(self):
        self.rowWidth = self.MAX_WIDTH - 2 * self.BLOCK_X_SPACER
        self.remainingRowWidth = self.rowWidth
        self.rowHeight = (self.MAX_HEIGHT - 2 * self.BLOCK_Y_SPACER)
        self.remainingRowHeight = self.rowHeight
        self.rightSideRowStart = self.BLOCK_X_SPACER * 2 + self.rowWidth
        self.buildNeighbourhood()
        self.initDrawing()
        #draw individual elements here
        self.drawBlocks()
        self.drawHouses()
        self.drawTents()
        
        
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
            if self.blockColourCounter == 5:
                self.blockColourCounter = 0
            else:
                self.blockColourCounter = self.blockColourCounter + 1
        return None

    def buildPackage(self, package):
        #Packages are implicitly represented in the output as blocks which are close together
        for module in package.modules:
            blockColour = self.PACKAGE_BLOCK_COLOURS[self.blockColourCounter]
            self.buildBlock(module, blockColour)

        return None

    def buildBlock (self, module, blockColour):
        #Modules are explicitly represented in the output as blocks (of 'grass') which surround the houses(classes) of that module
        blockRects = self.calculateBlockDimensions(module) #a list of tuples representing the rect dimensions for a single block
        colour = blockColour
        
        i = 0
        length = len(blockRects)
        while i < length:
     
            x = blockRects[i][0]
            y = blockRects[i][1]
            
            topLeft = self.blockCalculatePosition(x, y)
            block = Block(topLeft, x, y, colour)
            
            #Build Houses Here
            classes = module.getClasses()
            self.buildHouses(topLeft, classes)
            
            #Build Tents Here
            freeMethods = module.getFreeMethods()
            self.buildTents(freeMethods)
            
            self.blocks.append(block)
            
            i = i + 1
        return None
    '''
    Return a list of tuples (x,y,) which are the width, height of the rectangles needed to represent a block
    '''
    def calculateBlockDimensions(self, module):
        dimensions = []
        classes = module.getClasses()
        #Determine the width needed to represent a block
        totalWidth = 0
        width = 0
        
        for c in classes:
            totalWidth = totalWidth + self.HOUSE_X_SPACER
            width = self.calculateHouseWidth(c)
            totalWidth = totalWidth + width 
            
        freeMethods = int(module.getFreeMethods())
        if freeMethods != 0:
            spacers = (freeMethods) * self.TENT_X_SPACER
            freeMethodWidth = freeMethods * self.TENT_WIDTH
            totalWidth = totalWidth + spacers + freeMethodWidth - self.HOUSE_X_SPACER/2

    
        if totalWidth != 0:
            totalWidth = totalWidth + self.HOUSE_X_SPACER
            if totalWidth < self.MIN_BLOCK_WIDTH:
                totalWidth = self.MIN_BLOCK_WIDTH
        else:
            totalWidth = self.MIN_BLOCK_WIDTH
            
        lastHouseWidth = width
        tempTotalWidth = totalWidth
        
        if (tempTotalWidth != 0):
            if (tempTotalWidth >= lastHouseWidth):
                rect = (tempTotalWidth, self.BLOCK_HEIGHT)
            elif(lastHouseWidth > self.MIN_BLOCK_WIDTH):
                rect = (lastHouseWidth, self.BLOCK_HEIGHT)
            else:
                rect = (self.MIN_BLOCK_WIDTH, self.BLOCK_HEIGHT)
            dimensions.append(rect)
        return dimensions
    
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
    update currentY and remainingRowHeight after the addition of a new block in a new row
    '''
    def blockUpdateVerticalPosition(self, height):
        self.currentY = self.currentY + height + self.BLOCK_Y_SPACER
        self.remainingRowHeight = self.remainingRowHeight - height - self.BLOCK_Y_SPACER
        return None
    
    
    def buildHouses(self, topLeft, classes):
        self.blockCurrentX = topLeft[0] + self.HOUSE_X_SPACER
        self.blockCurrentY = topLeft[1] + self.HOUSE_Y_SPACER
        for c in classes:
            self.buildHouse(c, self.blockCurrentX, self.blockCurrentY)
            width = self.calculateHouseWidth(c)
            self.blockCurrentX = self.blockCurrentX + width + self.HOUSE_X_SPACER
        
        #set the currentY to the position needed for building the tents
        self.blockCurrentY = topLeft[1] + self.TENT_Y_SPACER
        return None

    def buildHouse(self, theClass, x, y):
        methods = theClass.getMethods()
        self.windowTallestWindow = self.calculateTallestWindow(methods)
        
        name = theClass.getName()
        
        length = self.calculateHouseHeight(theClass)
        width = self.calculateHouseWidth(theClass)
        y_pos = self.calculateHouseYPosition(y, length)
        topLeft = (x, y_pos)
        condition = int(theClass.getScore())
        theHouse = House(name, length, width, topLeft, condition)
        

        windows = self.buildWindows(methods, topLeft, width, length)
        theHouse.setWindows(windows)
        self.houses.append(theHouse)
        return None
    
    def calculateHouseYPosition(self, currentYPosition, height):
        #currentYPosition should be the y value of the top of a block + self.BlOCK_Y_SPACER
        baseYOfBlock = currentYPosition - self.HOUSE_Y_SPACER + self.BLOCK_HEIGHT
        height = height
        y = baseYOfBlock - height - self.HOUSE_Y_SPACER

        return y
    
    def calculateHouseWidth(self, theClass):
        methods = theClass.getMethods()
        width = self.HOUSE_X_SPACER
        
        for method in methods:
            parameter = int(method.getParameters())
            width = width + self.HOUSE_X_SPACER + parameter
    
        width = width + self.HOUSE_X_SPACER
        width = width / 2
        width = width + (1 * self.HOUSE_X_SPACER)
        return width
    
    def calculateHouseHeight(self, theClass):
        methods = theClass.getMethods()
        numberOfMethods = len(methods)
        firstHalf = int(numberOfMethods/2)
        
        if numberOfMethods % 2 != 0:
            firstHalf = firstHalf + 1
        
        topMethods = methods[0:firstHalf]
        bottomMethods = methods[firstHalf:numberOfMethods]
        
        tallestTopMethod = self.calculateTallestWindow(topMethods)
        tallestBottomMethod = self.calculateTallestWindow(bottomMethods)

        windowHeight = (tallestTopMethod + tallestBottomMethod)  + (self.WINDOW_X_SPACER * 4) +  self.HOUSE_DOOR_HEIGHT
        
        if windowHeight < self.HOUSE_MIN_HEIGHT:
            windowHeight = self.HOUSE_MIN_HEIGHT
        
        lines = int(theClass.getLines())
        if lines < self.HOUSE_MIN_HEIGHT:
            lines = self.HOUSE_MIN_HEIGHT
        
        if lines > windowHeight:
            height = lines
        else:
            height = windowHeight
        
        return height
    
    
    def buildWindows(self, methods, houseTopLeft, houseWidth, houseHeight):
        windows = []
        self.windowCurrentX = houseTopLeft[0] + self.WINDOW_X_SPACER
        self.windowCurrentY = houseTopLeft[1] + self.WINDOW_Y_SPACER
        self.sumWindowWidth = 0
        self.windowRows = self.calculateWindowRows(methods, houseWidth, houseHeight)

        for method in methods:
            window = self.buildWindow(method, houseTopLeft, houseWidth, houseHeight)
            windows.append(window)
            
        self.windowCurrentRow = 0
        return windows
    
    def buildWindow(self, method, houseTopLeft, houseWidth, houseHeight):
        dimensions = self.calculateWindowDimensions(method, houseTopLeft, houseWidth, houseHeight)
        topLeft = dimensions[0]
        width = dimensions[1]
        height = dimensions[2]
        colour = (179,242,239)
        window = Window(topLeft, width, height, colour)
        return window
    '''
    returns a tuple ((left, top), width, height) of the dimensions and position of a window
    '''
    def calculateWindowDimensions (self, method, houseTopLeft, houseWidth, houseHeight):
        width = int(method.getParameters()) * self.WINDOW_WIDTH_MULTIPLIER
        height = int(method.getLines()) * self.WINDOW_HEIGHT_MULTIPLIER
        houseXStart = houseTopLeft[0]
        houseXEnd = houseXStart + houseWidth
        
        rowHeight = self.windowTallestWindow
        #start at the top left, move right, then to new rows
        xSpaceRemaining = houseXEnd - self.windowCurrentX

        if width > xSpaceRemaining:
            # move down to new row
            self.windowCurrentY = self.windowCurrentY + rowHeight + self.WINDOW_Y_SPACER
            self.windowCurrentX = houseXStart + self.WINDOW_X_SPACER
        
            topLeft = (self.windowCurrentX, self.windowCurrentY)
            dimensions = (topLeft, width, height)
            
            self.windowCurrentX = self.windowCurrentX + width + self.WINDOW_X_SPACER
        else:
            #pass #create window here
            topLeft = (self.windowCurrentX, self.windowCurrentY)
            dimensions = (topLeft, width, height)
            self.windowCurrentX = self.windowCurrentX + width + self.WINDOW_X_SPACER
    
        return dimensions
    
    def calculateWindowRows(self, methods, houseWidth, houseHeight):
        rows = 0
        totalWindowWidth = self.WINDOW_X_SPACER
        for method in methods:
            width = int(method.getParameters()) * self.WINDOW_WIDTH_MULTIPLIER
            totalWindowWidth = totalWindowWidth + width + self.WINDOW_X_SPACER
        totalWindowWidth = totalWindowWidth + self.WINDOW_X_SPACER
        
        tempTotalWidth = totalWindowWidth
        while tempTotalWidth > 0:
            rows = rows + 1
            tempTotalWidth = tempTotalWidth - houseWidth
        return rows
    
    def calculateTallestWindow(self, methods):
        tallestMethod = 0
        for method in methods:
            height = int(method.getLines()) * self.WINDOW_HEIGHT_MULTIPLIER
            if height > tallestMethod:
                tallestMethod = height
        return tallestMethod
    
    def buildTents(self, freeMethods):
        i = 0
        while i < freeMethods:
            self.buildTent((self.blockCurrentX, self.blockCurrentY))
            self.blockCurrentX = self.blockCurrentX + self.TENT_WIDTH + self.TENT_X_SPACER
            i = i + 1
        return None
    
    def buildTent(self, topLeft):
        tent = Tent(topLeft)
        self.tents.append(tent)
        return None
    
    '''
    Initialize the output window
    '''
    def initDrawing(self):
        pygame.init()
        pygame.display.set_caption('Code Neighbourhood')
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
        
        #pygame.draw.rect(self.screen, colour, rect, 0)
        self.drawFilledRoundedRect(self.screen, colour, rect, self.BLOCK_CORNER_RADIUS)
        
        return None     
    
    def drawHouses(self):
        for house in self.houses:
            self.drawHouse(house)
        return None
    
    def drawHouse(self, house):
        condition = int(house.getCondition())
        #TODO Call different methods to draw different houses based upon condition
        if condition == 0:
            pass
        if condition == 1:
            pass
        if condition == 2:
            pass
        if condition == 3:
            pass
        if condition == 4:
            pass
        if condition == 5:
            pass
        if condition == 6:
            pass
        if condition == 7:
            pass
        if condition == 8:
            pass
        if condition == 9:
            pass
        else:
            self.drawPerfectHouse(house)
        return None
    
    def drawPerfectHouse(self, house):
        topLeft = house.getTopLeft()
        left = topLeft[0]
        top = topLeft[1]
        length = house.getLength()
        width = house.getWidth()
        randomIndex = randint(0,7)
        while randomIndex == self.lastHouseColourIndex:
            randomIndex = randint(0,7)
        self.lastHouseColourIndex = randomIndex
        
        colour = self.HOUSE_COLOURS[randomIndex]
        
        
        rect = (left, top, width, length)
        pygame.draw.rect(self.screen, colour, rect, 0)
        windows = house.getWindows()
        
        self.drawWindows(windows)
        
        self.drawHouseRoof(topLeft, width)
        self.drawHouseDoor(topLeft, width, length)
        
        return None
    
    def drawHouseRoof(self, topLeft, width):
        pointList = []
        pointList.append(topLeft)
        x2 = topLeft[0] + width /2
        y2 = topLeft[1] - self.HOUSE_ROOF_HEIGHT
        point2 = (x2, y2)
        pointList.append(point2)
        x3 = topLeft[0] + width
        y3 = topLeft[1]
        point3 = (x3, y3)
        pointList.append(point3)

        colour = self.HOUSE_DOOR_AND_ROOF_COLOUR
        pygame.draw.polygon(self.screen, colour, pointList, 0)
        
        return None
    
    def drawHouseDoor(self, topLeft, width, height):
        x_center = topLeft[0] + width/2
        y_baseline = topLeft[1] + height
        x = x_center - self.HOUSE_DOOR_WIDTH / 2
        y = y_baseline - self.HOUSE_DOOR_HEIGHT
        rect = (x,y,self.HOUSE_DOOR_WIDTH, self.HOUSE_DOOR_HEIGHT)
        colour = self.HOUSE_DOOR_AND_ROOF_COLOUR
        pygame.draw.rect(self.screen, colour, rect, 0)
        
        return None
    
    def drawWindows(self, windows):
        for window in windows:
            self.drawWindow(window)
    
    def drawWindow(self, window):
        topLeft = window.getTopLeft()
        width = window.getWidth()
        height = window.getHeight()
        colour = window.getColour()
        
        rect = (topLeft[0], topLeft[1], width, height)
        
        pygame.draw.rect(self.screen, colour, rect, 0)
        
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
    
    def drawTents(self):
        for tent in self.tents:
            self.drawTent(tent)
    
    def drawTent(self, tent):
        topLeft = tent.getTopLeft()
        left = topLeft[0]
        top = topLeft[1]
        baseline_y = top + self.TENT_HEIGHT
        width = self.TENT_WIDTH
        
        #draw the parallelogram
        points = [(left + width/4, top), (left + width/4 * 3, top), (left + width/2, baseline_y), (left, baseline_y)]
        pygame.draw.polygon(self.screen, self.TENT_COLOUR, points, 0)
        pygame.draw.polygon(self.screen, (0,0,0), points, 1)
        
        #draw the triangle
        points2 = [(left + width/4 * 3, top),(left + width, baseline_y),(left + width/2, baseline_y)]
        pygame.draw.polygon(self.screen, self.TENT_COLOUR, points2, 0)
        pygame.draw.polygon(self.screen, (0,0,0), points2, 1)
        
        #draw the centre pole
        pygame.draw.line(self.screen, self.HOUSE_DOOR_AND_ROOF_COLOUR, ((left + width/4 * 3) - 1, top), ((left + width/4 * 3) - 1, baseline_y), 2)
                                                                    
        return None
    '''
    Draws a filled rounded rectangle on the given surface.
    @radius: the radius of the corners as an integer
    @rect: the coords of the top-left corner and the dimensions of the rectangle as (x,y,width,length)
    '''
    def drawFilledRoundedRect(self, surface, colour, rect, radius):
        topLeftX = rect[0]
        topLeftY = rect[1]
        width = rect[2]
        length = rect[3]
    
        #draw the main rectangle
        mainTopLeftX = topLeftX + radius
        mainTopLeftY = topLeftY
        mainWidth = width - 2 * radius
        mainLength = length
        mainRect = (mainTopLeftX, mainTopLeftY, mainWidth, mainLength)
        pygame.draw.rect(surface, colour, mainRect,0)
        
        #draw the circles on the corners
        circleTopLeft = (topLeftX + radius, topLeftY + radius)
        circleTopRight = (topLeftX + width - radius, topLeftY + radius)
        circleBottomLeft = (topLeftX + radius, topLeftY + length - radius)
        circleBottomRight = (topLeftX + width - radius, topLeftY + length - radius)
        
        pygame.draw.circle(surface, colour, circleTopLeft, radius, 0)
        pygame.draw.circle(surface, colour, circleTopRight, radius, 0)
        pygame.draw.circle(surface, colour, circleBottomLeft, radius, 0)
        pygame.draw.circle(surface, colour, circleBottomRight, radius, 0)
        
        #draw the side rectangles
        leftRect = (topLeftX, topLeftY + radius, radius, length - 2 * radius)
        rightRect = (topLeftX + width - radius, topLeftY + radius, radius, length - 2 * radius)
        pygame.draw.rect(surface, colour, leftRect, 0)
        pygame.draw.rect(surface, colour, rightRect, 0)
        
        return None  
    
class House(object):
    name = ''
    length = 0
    width = 0
    topLeft = (0,0)
    condition = 0
    windows = []
    
    def __init__(self, name, length, width, topLeft, condition):
        self.name = name
        self.length = length
        self.width = width
        self.topLeft = topLeft
        self.condition = condition
        
    def getName(self):
        return self.name
    
    def getLength(self):
        return self.length
    
    def getWidth(self):
        return self.width
    
    def getTopLeft(self):
        return self.topLeft
    
    def getCondition(self):
        return self.condition
    
    def setWindows(self, windows):
        self.windows = windows
        
    def getWindows(self):
        return self.windows

    
class Window(object):
    height = 0
    width = 0
    colour = (0,0,0)
    topLeft = (0,0)
    
    def __init__(self, topLeft, width, height, colour):
        self.height = height
        self.width = width
        self.colour = colour
        self.topLeft = topLeft
    
    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width
    
    def getColour(self):
        return self.colour
    
    def getTopLeft(self):
        return self.topLeft
    
        
class Tent(object):
    topLeft = (0,0)
    
    def __init__(self, topLeft):
        self.topLeft = topLeft
        
    def getTopLeft(self):
        return self.topLeft
        
class Powerline(object):
    start = (0,0)
    finish = (0,0)
    
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish

class Clothesline(object):
    start = (0,0)
    finish = (0,0)
    
    def __init__(self, start, finish):
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
