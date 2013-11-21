'''
Created on Nov 20, 2013

@author: ericchu
'''
from CodeNeighbourhood.Visualizer.Renderer import Renderer
from CodeNeighbourhood.Visualizer.Renderer import House
from CodeNeighbourhood.Visualizer.Renderer import Window
from CodeNeighbourhood.Visualizer.Renderer import Tent
from CodeNeighbourhood.Visualizer.Renderer import Block
from CodeNeighbourhood.Visualizer.Renderer import PackageBlock
from CodeNeighbourhood.Analyzer.XMLParser import XMLParser
import unittest

''' Unit test class for the package Visualizer ''' 

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        afile = open("TestXMLSample.xml", "r")
        self.xmlString = "".join(afile.readlines())
        afile.close()
        self.xmlparser = XMLParser(self.xmlString)
        self.xmlPackages = self.xmlparser.getPackages()
        self.renderer = Renderer(self.xmlPackages)
            
    def testHouseConstructor(self):
        house = House("TheHouseName", 4, 5, (5,3), 7)
        self.failUnless(house.getName() == "TheHouseName")
        self.failUnless(house.getLength() == 4)
        self.failUnless(house.getWidth() == 5)
        self.failUnless(house.getTopLeft() == (5,3))
        self.failUnless(house.getCondition() == 7)
        
    def testWindowConstructor(self): 
        window = Window((6,8), 4, 65, (54,84,95))
        self.failUnless(window.getTopLeft() == (6,8))
        self.failUnless(window.getWidth() == 4)
        self.failUnless(window.getHeight() == 65)
        self.failUnless(window.getColour() == (54,84,95))
        
    def testTentConstructor(self):
        tent = Tent((9,4))
        self.failUnless(tent.getTopLeft() == (9,4))
        
    def testBlockConstructor(self):
        block = Block((9,7), 2, 52, (53,63,12))
        self.failUnless(block.getTopLeft() == (9,7))
        self.failUnless(block.getWidth() == 2)
        self.failUnless(block.getLength() == 52)
        self.failUnless(block.getColour() == (53,63,12))
    
    def testPackageBlockConstructor(self):
        house0 = House("house0", 4, 5, (5,3), 7)
        house1 = House("house1", 4, 5, (5,3), 7)
        house2 = House("house2", 4, 5, (5,3), 7)
        house3 = House("house3", 4, 5, (5,3), 7)
        houses = [house0, house1, house2, house3]
        
        block0 = Block((9,7), 0, 52, (53,63,12))
        block1 = Block((9,7), 1, 52, (53,63,12))
        block2 = Block((9,7), 2, 52, (53,63,12))
        block3 = Block((9,7), 3, 52, (53,63,12))
        blocks = [block0, block1, block2, block3]

        packageBlock = PackageBlock(blocks, houses)
        
        blockWidths = []
        for ablock in packageBlock.getBlocks():
            blockWidths.append(ablock.getWidth())
        self.failUnless(blockWidths == [0, 1, 2, 3])
        
        houseNames = []
        for ahouse in packageBlock.getHouses():
            houseNames.append(ahouse.getName())
        self.failUnless(houseNames == ['house0', 'house1', 'house2', 'house3'])
    
    def testCalculateTallestWindow(self):
        methods = self.xmlPackages[0].getModules()[1].getClasses()[1].getMethods()
        self.failUnless(self.renderer.calculateTallestWindow(methods) == 87)
        
    def testBuildWindow(self):
        method = self.xmlPackages[0].getModules()[1].getClasses()[1].getMethods()[3]
        window = self.renderer.buildWindow(method, (58,89), 2, 95)
        self.failUnless(window.getTopLeft() == (0,0))
        self.failUnless(window.getWidth() == 0)
        self.failUnless(window.getHeight() == 9)
        self.failUnless(window.getColour() == (179, 242, 239))
        
    def testCalculateHouseHeight(self):
        aclass0 = self.xmlPackages[0].getModules()[1].getClasses()[0]
        aclass = self.xmlPackages[0].getModules()[1].getClasses()[1]
        self.failUnless(self.renderer.calculateHouseHeight(aclass0) == 31)
        self.failUnless(self.renderer.calculateHouseHeight(aclass) == 117)
        
    def testCalculateHouseWidth(self):
        aclass0 = self.xmlPackages[0].getModules()[1].getClasses()[0]
        aclass = self.xmlPackages[0].getModules()[1].getClasses()[1]
        self.failUnless(self.renderer.calculateHouseWidth(aclass0) == 30)
        self.failUnless(self.renderer.calculateHouseWidth(aclass) == 134)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()