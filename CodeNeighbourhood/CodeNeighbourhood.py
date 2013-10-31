'''
Created on Oct 31, 2013

@author: Mike and Jon
'''
import sys
from CodeToXML import DirectoryCrawler

from Visualizer.CustomTypes import *
from Visualizer.Renderer import *
from Visualizer.XMLParser import *


def directoryCrawl():
    XMLString = DirectoryCrawler.directoryCrawl('pyntaCode')
    #print XMLString
    
    XMLParser1 = XMLParser(XMLString)
    
    packages = XMLParser1.getPackages()
    renderer1 = Renderer(packages)
    renderer1.renderNeighbourhood()
    return None

if __name__ == '__main__':
    directoryCrawl()