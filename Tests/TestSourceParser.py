'''
Created on Nov 17, 2013

@author: ericchu
'''
from CodeNeighbourhood.SourceParser.ModuleParser import ModuleParser
from CodeNeighbourhood.SourceParser.ClassLister import ClassLister
import xml.etree.cElementTree as Tree
import unittest

''' Unit test class for the package SourceParser ''' 

class TestSourceParser(unittest.TestCase):
    
    ''' Constructs ModuleParser object in preparation for tests for SourceParser; 
        takes TestSample.py as sample input'''
    def setUp(self):
        root = Tree.Element("CodeBase")
        package = Tree.SubElement(root, "Package", {'name' : 'package1'})
        module = Tree.SubElement(package, "Module", {'name' : 'TestSample'})
        self.parser = ModuleParser(module, "TestSample.py", ["SampleClass","SampleClass2"])

    ''' *** ModuleParser Tests *** ''' 

    ''' tests ModuleParser::isEmpty to ensure that empty lines are properly identified '''
    def testMPisEmpty(self):
        self.failUnless(not self.parser.isEmpty(20)) 
        self.failUnless(self.parser.isEmpty(19))
        self.failUnless(self.parser.isEmpty(21))
        
    ''' tests ModuleParser::CommentLine to ensure that comments are properly identified '''
    def testMPisCommentLine(self):
        self.failUnless(self.parser.isCommentLine(19))
        self.failUnless(not self.parser.isCommentLine(20))
        self.failUnless(not self.parser.isCommentLine(21))
        
    ''' tests ModuleParser::indentationLevel to ensure that indentation levels are properly identified '''
    def testMPindentationLevel(self):
        self.failUnless(self.parser.indentationLevel(77, 0))
        self.failUnless(not self.parser.indentationLevel(77, 1))
        self.failUnless(self.parser.indentationLevel(82, 4))
        self.failUnless(not self.parser.indentationLevel(82, 5))
        
    ''' tests ModuleParser::countLines to ensure that number of lines are counted correctly '''
    def testMPCountLines(self):
        self.failUnless(self.parser.countLines(82, 97) == 13)
        self.failUnless(self.parser.countLines(75, 81) == 4)

    ''' tests ModuleParser::countDocumentation to ensure that number of documentation lines above method definitions are
        correctly counted '''
    def testMPCountDocumentation(self):
        self.failUnless(self.parser.countDocumentation(102) == 3)
        self.failUnless(self.parser.countDocumentation(111) == 2)
        
    ''' tests ModuleParser::countComment to ensure that number of comment lines are correctly counted '''   
    def testMPCountComment(self):
        self.failUnless(self.parser.countComments(93, 103) == 3)
        self.failUnless(self.parser.countComments(107, 115) == 4)
        
    ''' *** ClassLister Tests *** ''' 
        
    ''' tests ClassLister::findClassInModule to ensure all class declarations are properly identified '''   
    def testCLfindClassInModule(self):
        classLister = ClassLister("")
        classLister.findClassInModule("TestSample.py", "Tests")
        self.failUnless(classLister.list == ['SampleClass', 'SampleClass2'])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()