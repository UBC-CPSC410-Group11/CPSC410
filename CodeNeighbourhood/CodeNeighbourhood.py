'''
Created on Oct 31, 2013

@author: Mike and Jon
'''
from SourceParser.DirectoryCrawler import directoryCrawl
from Analyzer.CustomTypes import *

from Visualizer.Renderer import Renderer
from Analyzer.XMLParser import *

def main():
    XMLString = directoryCrawl('pyntaCode')
    
    XMLParser1 = XMLParser(XMLString)
    
    packages = XMLParser1.getPackages()
    outCalls = setInModuleBools(packages)
    
    
    renderer1 = Renderer(packages)
    renderer1.renderNeighbourhood()
    return None

if __name__ == '__main__':
    main()