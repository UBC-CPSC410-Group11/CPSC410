'''
Created on Oct 23, 2013

@author: Mike
'''
from Parser.CustomTypes import *


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
        
    '''
    Call this method to generate the output image
    '''
    def renderNeighbourhood(self):
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
        #TODO
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


#FOR TESTTING
def main():
    renderer = Renderer()
    
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

    #add the packages
    renderer.packages.append(package1)
    renderer.packages.append(package2)
    renderer.packages.append(package3)
    
    renderer.renderNeighbourhood()
    return None
                
        
        
if __name__ == "__main__":
        main()
  
        
        

