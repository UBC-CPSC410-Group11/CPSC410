'''
Created on Nov 17, 2013

@author: ericchu
'''
from CodeNeighbourhood.SourceParser.ModuleParser import ModuleParser as ModuleParser
import xml.etree.cElementTree as Tree
import unittest


class Test(unittest.TestCase):
    
    root = Tree.Element("CodeBase")
    package = Tree.SubElement(root, "Package", {'name' : 'package1'})
    module = Tree.SubElement(package, "Module", {'name' : 'TestSample'})
    parser = ModuleParser(module, "TestSample.py")

    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()