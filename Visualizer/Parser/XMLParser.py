'''
Created on 2013-10-22

@author: jonrl33
'''
from xml.dom.minidom import parse
from CustomTypes import Package, Module, Class, Method

class XMLParser(object):
    packages = []
    
    def __init__(self, in_File):
        self.parseFile(in_File)
        
        
    def parseFile(self, in_File):
        doc = parse(in_File)
        for node in doc.getElementsByTagName("package"):
            pass
    
        
    def getPackages(self):
        return self.packages