'''
Created on Nov 17, 2013

@author: ericchu
'''
from CodeNeighbourhood.SourceParser.ModuleParser import ModuleParser as ModuleParser
import xml.etree.cElementTree as Tree
import unittest


class TestSourceParser(unittest.TestCase):
    
    def setUp(self):
        root = Tree.Element("CodeBase")
        package = Tree.SubElement(root, "Package", {'name' : 'package1'})
        module = Tree.SubElement(package, "Module", {'name' : 'TestSample'})
        self.parser = ModuleParser(module, "TestSample.py")

    def tearDown(self):
        pass


    def testMPisEmpty(self):
        self.failUnless((not self.parser.isEmpty(20)) 
                        and self.parser.isEmpty(19) 
                        and self.parser.isEmpty(21))
        
    def testMPisCommentLine(self):
        self.failUnless(self.parser.isCommentLine(19)
                        and (not self.parser.isCommentLine(20))
                        and (not self.parser.isCommentLine(21)))
        
    def testMPindentationLevel(self):
        self.failUnless(self.parser.indentationLevel(77, 0)
                        and (not self.parser.indentationLevel(77, 1))
                        and self.parser.indentationLevel(82, 4)
                        and (not self.parser.indentationLevel(82, 5)))
        
    def testMPCountLines(self):
        self.failUnless(self.parser.countLines(82, 97) == 13
                        and self.parser.countLines(75, 81) == 4)

    def testMPCountDocumentation(self):
        self.failUnless(self.parser.countDocumentation(102) == 3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()