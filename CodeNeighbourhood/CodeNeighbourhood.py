'''
Created on Oct 31, 2013

@author: Mike and Jon
'''
from CodeToXML import DirectoryCrawler

from Visualizer.Renderer import Renderer
from Visualizer.XMLParser import XMLParser


def main():
    XMLString = DirectoryCrawler.directoryCrawl('pyntaCode')
    #print XMLString
    
    XMLParser1 = XMLParser(XMLString)
    
    packages = XMLParser1.getPackages()
    renderer1 = Renderer(packages)
    renderer1.renderNeighbourhood()
    return None

if __name__ == '__main__':
    main()