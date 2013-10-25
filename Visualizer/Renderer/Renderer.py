'''
Created on Oct 23, 2013

@author: Mike
'''
class Renderer(object):
    MAX_WIDTH = 1200
    MAX_HEIGHT = 900
    HOUSE_SPACER = 10
    BLOCK_X_SPACER = 10
    BLOCK_Y_SPACER = 10

    packages = []
    packageCount = 0
    
    houses = []
    windows = []
    tents = []
    powerlines = []
    clotheslines = []
    fountain = {}
    blocks = []
    
    width = 0
    height = 0
    currentX = 0
    currentY = 0
    currentHouseTopLeft = (0,0)
    newBlock = 1
    
    def _init_(self, packages):
        self.packages = packages
        self.packageCount = len(packages)
        
    def buildPackage(self, package):
        #TODO Implement
        return None
    
    def buildBlock (self, module):
        #TODO Implement
        return None
        
    def buildHouse(self, theClass):
        #TDOO Implement
        return None
    
    def buildWindow(self, method):
        #TODO Implement
        return None
    
    #May need more helpers...
    
    def drawBlock(self, block):
        #TODO Implement
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
    numOfRows = 0
    topLeft = (0,0)
    endXValue = 0
    colour = (0,0,0)
    
    def __init__(self, numOfRows, topLeft, endXValue, colour):
        self.numOfRows = numOfRows
        self.topLeft = topLeft
        self.endXValue = endXValue
        self.colour = colour

  
        
        

