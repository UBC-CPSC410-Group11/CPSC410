'''
Created on Oct 23, 2013

@author: Mike
'''
from Analyzer.CustomTypes import *
import pygame
import sys

class RendererFacade(object):
    packages = []
    imageDimensions = {}
    
    
    def __init__(self, packages):
        self.packages = packages
    
    def render(self):
        renderer = Renderer(self.packages)
        self.imageDimensions = renderer.renderNeighbourhood()
        imageGenerator = ImageGenerator(self.imageDimensions)
        imageGenerator.generateImage(renderer)
        return None

class ImageGenerator(object):
    imageDimensions = {}
    NUMBER_OF_IMAGES_PER_ROW = 3

    
    def __init__(self, imageDimensions):
        self.imageDimensions = imageDimensions

    '''
    Generates and displays the main output image
    '''
    def generateImage(self, renderer):
        dimensionsAndRowHeight = self.calculateImageDimensions(self.NUMBER_OF_IMAGES_PER_ROW)
        dimensions = dimensionsAndRowHeight[0]
        rowHeight = dimensionsAndRowHeight[1]
        mainImage = pygame.Surface(dimensions)
        mainImage.fill(Renderer.BACKGROUND_COLOUR)
        
        screen = renderer.getScreen()
        
        currentX = 0
        currentY = 0
        i = 1

        for imageDimension in self.imageDimensions:
            imageIndex = imageDimension[0]
            dimensions = imageDimension[1]
            width = dimensions[0]
            #height = dimensions[1]
            image = self.loadImage(imageIndex)
            mainImage.blit(image,(currentX,currentY))
            if i < self.NUMBER_OF_IMAGES_PER_ROW:
                currentX = currentX + width
                i = i + 1
            else:
                currentX = 0
                currentY = currentY + rowHeight
                i = 1
        
        scaledDimensions = self.calculateScaledImageSize(dimensions)
        scaledMainImage = pygame.transform.scale(mainImage, (scaledDimensions[0], scaledDimensions[1]))

        screen.blit(scaledMainImage,(0,0))
        pygame.display.update()
        
        control = 1
        while control:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                    control = 0
    
    '''
    Returns a tuple (x,y) of dimensions for the largest possible image (with constrained proportions) within the output window.
    '''          
    def calculateScaledImageSize(self, dimensions):
        windowWidth = Renderer.MAX_WIDTH
        windowHeight = Renderer.MAX_HEIGHT
        imageWidth = dimensions[0]
        imageHeight = dimensions[1]
        
        widthDifference = windowWidth - imageWidth
        heightDifference = windowHeight - imageHeight
        
        if widthDifference <= heightDifference:
            newWidth = windowWidth 
            newHeight = int((imageWidth/imageHeight) * newWidth)
            newDimensions = (newWidth, newHeight)
            
        else:
            newHeight = windowHeight
            newWidth = int((imageHeight/imageWidth) * newHeight)
            newDimensions = (newWidth, newHeight)
            
        return newDimensions
        
    '''
    returns a pygame.Surface of a loaded image
    '''
    def loadImage(self, imageIndex):
        index = str(imageIndex)
        extension = Renderer.FILE_EXTENSION
        fileName = 'temp_image' + index + extension
        theImage = pygame.image.load(fileName)
        
        return theImage

    '''
    returns a tuple ((x,y),rh) of the main output image's width, height, and rowHeight
    '''        
    def calculateImageDimensions(self, numberOfImagesPerRow):
        rowWidths = []
        rowHeights = []
        i = 0
        widthAccumulator = 0
        maxHeight = 0
        for imageDimension in self.imageDimensions:
            dimensions = imageDimension[1]
            width = dimensions[0]
            height = dimensions[1]
            if i < numberOfImagesPerRow:
                if height > maxHeight:
                    maxHeight = height
                widthAccumulator = widthAccumulator + width
                i = i + 1
            else:
                rowWidths.append(widthAccumulator)
                rowHeights.append(maxHeight)
                maxHeight = 0
                widthAccumulator = width
                i = 1
        rowHeights.append(maxHeight)
        rowWidths.append(widthAccumulator)
        imageWidth = max(rowWidths)
        imageHeight = 0
        for rh in rowHeights:
            imageHeight = imageHeight + rh
        
        maxRowHeight = max(rowHeights)
        dimensions = ((imageWidth, imageHeight), maxRowHeight)
        return dimensions
    
class Renderer(object):
    MAX_WIDTH = 900
    MAX_HEIGHT = 900
    
    IMAGE_MIN_WIDTH = 300
    
    HOUSE_X_SPACER = 20
    HOUSE_Y_SPACER = 20
    BLOCK_X_SPACER = 20 
    BLOCK_Y_SPACER = 50 
    BLOCK_HEIGHT = 100
    BLOCK_CORNER_RADIUS = 15
    MIN_BLOCK_WIDTH = 80
    
    HOUSE_MIN_HEIGHT = 15
    HOUSE_MIN_WIDTH = 30
    HOUSE_ROOF_HEIGHT = 20
    HOUSE_DOOR_HEIGHT = 20
    HOUSE_DOOR_WIDTH = 10
    
    WINDOW_X_SPACER = 4
    WINDOW_Y_SPACER = 5
    WINDOW_MIN_HEIGHT = 5
    WINDOW_MIN_WIDTH = 5
    WINDOW_WIDTH_MULTIPLIER = 10
    WINDOW_HEIGHT_MULTIPLIER = 3
    
    TENT_WIDTH = 40
    TENT_HEIGHT = 20
    TENT_COLOUR = (228, 219, 137)
    TENT_X_SPACER = 30
    TENT_Y_SPACER = 50
    
    BACKGROUND_COLOUR = (169,167,146)
    PACKAGE_BLOCK_COLOURS = [ (68,131,7), (141,153,109),(87,158,18), (96,149,84), (141,173,109), (49,158,55), (127,153,109)]
    HOUSE_COLOURS = [(0,0,0), (255,0,0), (220,20,70), (253,106,8), (247,255,0), (51,255,0), (6, 222, 222), (87,121,255), (228,222,255), (246,248,253)]
    HOUSE_DOOR_AND_ROOF_COLOUR = (115,99,87)
    
    FILE_EXTENSION = '.jpg'
    
    screen = {}
    packages = []
    houses = []
    tents = []
    blocks = []
    
    surfaceWidth = 0
    surfaceHeight = 0
    
    currentX = BLOCK_X_SPACER
    currentY = BLOCK_Y_SPACER * 2
    rowWidth = 0
    remainingRowWidth = 0
    remainingRowHeight = 0
    blockColourCounter = 0
    lastHouseColourIndex = 0
    blockCurrentX = 0
    blockCurrentY = 0
    windowCurrentX = 0
    windowCurrentY = 0
    windowCurrentRow = 0
    windowTallestWindow = 0
    
    imageDimensions = []
    
    def __init__(self, packages):
        self.packages = packages
    
    def getScreen(self):
        return self.screen
      
    '''
    Renders a neighbourhood for each package and saves it to a temp file 
    '''
    def renderNeighbourhood(self):
        
        self.initDrawing()
        
        i = 0
        numberOfPackages = len(self.packages)
        
        while i < numberOfPackages:
            self.resetScreen()
            dimensions = self.calculateImageDimensions(self.packages[i])
            self.surfaceWidth = dimensions[0]
            self.surfaceHeight = dimensions[1]
            if self.surfaceWidth < self.IMAGE_MIN_WIDTH:
                self.surfaceWidth = self.IMAGE_MIN_WIDTH
            self.resetAllVariables()
            numberOfBlockColours = len(self.PACKAGE_BLOCK_COLOURS)
            self.blockColourCounter = i
            if self.blockColourCounter > numberOfBlockColours:
                self.blockColourCounter = 0
            self.buildNeighbourhood(self.packages[i])
            self.drawBlocks()
            self.drawHouses()
            self.drawTents()
            self.saveScreen(i)
            imageDimension = (i, (self.surfaceWidth,self.surfaceHeight))
            self.imageDimensions.append(imageDimension)
            
            i = i + 1
        
        return self.imageDimensions
    
    def initDrawing(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAX_WIDTH,self.MAX_HEIGHT))
        pygame.display.set_caption('Code Neighbourhood')
        
        return None
    
    def resetScreen(self):
        screen2 = pygame.Surface((self.MAX_WIDTH,self.MAX_HEIGHT))
        screen2.fill(self.BACKGROUND_COLOUR)
        self.screen.blit(screen2,(0,0))
        return None
    
    def saveScreen(self, i):
        extension = self.FILE_EXTENSION
        strId = str(i)
        fileName = 'temp_image'+ strId + extension
        saveScreen = pygame.Surface((self.surfaceWidth, self.surfaceHeight))
        saveScreen.blit(self.screen, (0,0), (0,0,self.surfaceWidth, self.surfaceHeight))
        pygame.image.save(saveScreen, fileName)
                   
    
    def resetAllVariables(self):
        self.currentX = self.BLOCK_X_SPACER
        self.currentY = self.BLOCK_Y_SPACER * 2
        self.rowWidth = 0
        self.remainingRowWidth = 0
        self.remainingRowHeight = 0
        self.blockColourCounter = 0
        self.lastHouseColourIndex = 0
        self.blockCurrentX = 0
        self.blockCurrentY = 0
        self.windowCurrentX = 0
        self.windowCurrentY = 0
        self.windowCurrentRow = 0
        self.windowTallestWindow = 0
        
        self.houses = []
        self.tents = []
        self.blocks = []
        
        self.rowWidth = self.surfaceWidth - 2 * self.BLOCK_X_SPACER
        self.remainingRowWidth = self.rowWidth
        self.rowHeight = (self.surfaceHeight - 2 * self.BLOCK_Y_SPACER)
        self.remainingRowHeight = self.rowHeight
        
        
        return None
    
    def buildNeighbourhood(self, package):
        self.buildPackage(package)
        return None
    
    def calculateImageDimensions(self, package):
        modules = package.getModules()
        blockRects = []
        for module in modules:
            blockRect = self.calculateBlockDimensions(module)
            blockRects.append(blockRect)
        
        width = self.calculateImageWidth(blockRects)
        height = self.calculateImageHeight(blockRects, width)
        return (width, height)
    
    def calculateImageWidth(self, blockRects):
        widestBlock = 0
        sumOfWidths = 0
        for br in blockRects:
            if len(br) > 0:
                x_val = br[0][0]
                sumOfWidths = sumOfWidths + x_val
                if x_val > widestBlock:
                    widestBlock = x_val
        width = widestBlock + 4 * self.BLOCK_X_SPACER
        return width
    
    def calculateImageHeight(self, blockRects, width):
        numberOfRows = 1
        blockWidths = []
        widthRemaining = width - self.BLOCK_X_SPACER * 2
        
        for br in blockRects:
            if len(br) > 0:
                blockWidth = br[0][0]
                blockWidths.append(blockWidth)
          
        i = 0
        while i < len(blockWidths):
            widthRemaining = widthRemaining - blockWidths[i] -  self.BLOCK_X_SPACER
            if i != len(blockWidths) - 1:
                if widthRemaining < blockWidths[i + 1]:
                    numberOfRows = numberOfRows + 1
                    widthRemaining = width - self.BLOCK_X_SPACER * 2
            
            i = i + 1
        
        height = 1 * self.BLOCK_Y_SPACER + numberOfRows * self.BLOCK_HEIGHT + (numberOfRows) * self.BLOCK_Y_SPACER
        return height

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
        # else:   #Uncomment this to show blocks with no classes or free methods
        #     totalWidth = self.MIN_BLOCK_WIDTH
            
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
                self.currentX = self.BLOCK_X_SPACER
                self.blockUpdateVerticalPosition(height)
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
        print condition
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
        width = self.WINDOW_X_SPACER
        for method in methods:
            parameter = int(method.getParameters())
            width = width + self.WINDOW_X_SPACER + (parameter * self.WINDOW_WIDTH_MULTIPLIER)
        
        if width < self.HOUSE_MIN_WIDTH:
            width = self.HOUSE_MIN_WIDTH
        
        
        return width 
    
    def calculateHouseHeight(self, theClass):
        methods = theClass.getMethods()

        tallestMethod = self.calculateTallestWindow(methods)
        
        windowHeight = tallestMethod
        
        lines = int(theClass.getLines())

        if lines > windowHeight:
            height = lines
        else:
            height = windowHeight
        
        height = height + self.HOUSE_DOOR_HEIGHT + 2 * self.WINDOW_Y_SPACER
        if height < self.HOUSE_MIN_HEIGHT:
            height = self.HOUSE_MIN_HEIGHT
        return height
    
    
    def buildWindows(self, methods, houseTopLeft, houseWidth, houseHeight):
        windows = []
        self.windowCurrentX = houseTopLeft[0] + self.WINDOW_X_SPACER
        self.windowCurrentY = houseTopLeft[1] + self.WINDOW_Y_SPACER
        self.sumWindowWidth = 0

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
        topLeft = (self.windowCurrentX, self.windowCurrentY)
        dimensions = (topLeft, width, height)
        self.windowCurrentX = self.windowCurrentX + width + self.WINDOW_X_SPACER
    
        return dimensions
   
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
        self.drawFilledRoundedRect(self.screen, colour, rect, self.BLOCK_CORNER_RADIUS)
        
        return None     
    
    def drawHouses(self):
        for house in self.houses:
            self.drawHouse(house)
        return None
    
    def drawHouse(self, house):
        topLeft = house.getTopLeft()
        left = topLeft[0]
        top = topLeft[1]
        length = house.getLength()
        width = house.getWidth()
        condition = int(house.getCondition()) - 1
        colour = self.HOUSE_COLOURS[condition]
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
    Draws a filled rounded rectangle on the given screen.
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
    
class PackageBlock(object):
    blocks = []
    houses = []
    topLeft = (0,0)
    
    def __init__(self, blocks, houses):
        self.blocks = blocks
        self.houses = houses
        
    def getBlocks(self):
        return self.blocks
    
    def getHouses(self):
        return self.houses
    
    def setTopLeft(self, topLeft):
        self.topLeft = topLeft
        
    def getTopLeft(self):
        return self.topLeft

        
