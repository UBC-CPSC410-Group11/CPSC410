'''
    Created on 08.11.2013
    
    @author: Chris
'''


import os


''' Is able to return a list of tuples of (class, packageName) '''
class ClassLister():


    def __init__(self, argv):
        self.argv = argv
        self.list = []


    ''' Opens the given module and searches for class names to add to 
        the list of (class, packageName) - tuples '''
    def findClassInModule(self, filePath, packageName):
        f = open(filePath)
        code = f.readlines()
        f.close()
        lineCounter = len(code)
    
        for i in range(0, lineCounter):
            currLine = code[i].strip()
            words = currLine.split()
            if (currLine.startswith('class ') and (len(words) >= 2)):
                className = ''
                for j in range(0, len(words[1])):
                    if words[1][j] == '(' or words[1][j] == ':':
                        break
                    className += words[1][j]
                self.list.append(className)
    
    

    ''' Crawls through the given package and calls findClassInModule() 
        for every module (= .py-file) it finds '''
    def crawlPackage(self, dirPath, packageName):
        for path, _, files in os.walk(dirPath):
            for f in files:
                if path == dirPath:
                    self.findClassInModule(os.path.join(dirPath, f), packageName)



    ''' Crawls through the given directory and calls crawlPackage() 
        for every package (= folder) it finds '''
    def returnList(self):
        for path, dirs, _ in os.walk(self.argv):
            for d in dirs:
                self.crawlPackage(os.path.join(path, d), d)

        return self.list

