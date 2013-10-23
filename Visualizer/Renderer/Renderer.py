'''
Created on Oct 23, 2013

@author: Mike
'''

class RenderNeighbourhood(object):
    packages = []
    packageCount = 0
    
    def _init_(self, packages):
        self.packages = packages
        self.packageCount = len(packages)
        
