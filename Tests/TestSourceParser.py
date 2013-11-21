'''
Created on Nov 17, 2013

@author: ericchu
'''
from CodeNeighbourhood.SourceParser.ModuleParser import ModuleParser
import xml.etree.cElementTree as Tree
import unittest

''' Unit test for the package SourceParser
; takes TestSample.py as input to test basic functions used in parsing the source code'''
class TestSourceParser(unittest.TestCase):
    
    def setUp(self):
        root = Tree.Element("CodeBase")
        package = Tree.SubElement(root, "Package", {'name' : 'package1'})
        module = Tree.SubElement(package, "Module", {'name' : 'TestSample'})
        self.parser = ModuleParser(module, "TestSample.py", ["SampleClass","SampleClass2"])

    def tearDown(self):
        pass


    def testMPisEmpty(self):
        self.failUnless(not self.parser.isEmpty(20)) 
        self.failUnless(self.parser.isEmpty(19))
        self.failUnless(self.parser.isEmpty(21))
        
    def testMPisCommentLine(self):
        self.failUnless(self.parser.isCommentLine(19))
        self.failUnless(not self.parser.isCommentLine(20))
        self.failUnless(not self.parser.isCommentLine(21))
        
    def testMPindentationLevel(self):
        self.failUnless(self.parser.indentationLevel(77, 0))
        self.failUnless(not self.parser.indentationLevel(77, 1))
        self.failUnless(self.parser.indentationLevel(82, 4))
        self.failUnless(not self.parser.indentationLevel(82, 5))
        
    def testMPCountLines(self):
        self.failUnless(self.parser.countLines(82, 97) == 13)
        self.failUnless(self.parser.countLines(75, 81) == 4)

    def testMPCountDocumentation(self):
        self.failUnless(self.parser.countDocumentation(102) == 3)
        self.failUnless(self.parser.countDocumentation(111) == 2)
        
    def testMPCountComment(self):
        self.failUnless(self.parser.countComments(93, 103) == 3)
        self.failUnless(self.parser.countComments(107, 115) == 4)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()