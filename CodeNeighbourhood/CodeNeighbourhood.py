'''
Created on Oct 31, 2013

@author: Mike and Jon
'''
import sys
from CodeToXML import DirectoryCrawler

from Visualizer.CustomTypes import *
from Visualizer.Renderer import *
from Visualizer.XMLParser import *

def CodeNeighbourhood(object):
    

    def __init__(self):
        pass


def main():
    #XMLString = DirectoryCrawler.directoryCrawl(sys.argv[1])
    #print XMLString
    
    XMLParser1 = XMLParser('C:\Users\Mike\git\CPSC410\SampleInput.xml')
    packages = XMLParser1.getPackages()
    renderer1 = Renderer(packages)
    renderer1.renderNeighbourhood()
    return None

if __name__ == '__main__':
    main()