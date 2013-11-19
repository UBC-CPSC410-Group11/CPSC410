'''
Created on Oct 31, 2013
     
@author: Mike and Jon
'''
from SourceParser.DirectoryCrawler import directoryCrawl
from Analyzer.CustomTypes import *
from Visualizer.Renderer import RendererFacade

from Analyzer.XMLParser import *
from Analyzer.ScoreQuality import *

def main():
    XMLString = directoryCrawl('pyntaCode')
    
    XMLParser1 = XMLParser(XMLString)
    
    packages = XMLParser1.getPackages()
    setInModuleBools(packages)
    qScore = ScoreQuality()
    qScore.scorePackages(packages)
    
    rendererFacade = RendererFacade(packages)
    rendererFacade.render()

    return None

if __name__ == '__main__':
    main()
