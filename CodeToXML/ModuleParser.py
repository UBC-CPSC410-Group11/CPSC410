'''
Created on 21.10.2013

@author: Chris
'''

import xml.etree.cElementTree as Tree
import sys
import os


''' here the file parsing takes place '''
class ModuleParser():
    
    ''' the ModuleParser object receives the node of the xml tree to append to
    and the filePath of the file to be parsed ''' 
    def __init__(self, moduleRoot, filePath):
        self.moduleRoot = moduleRoot
        f = open(filePath)
        self.code = f.readlines()
        f.close()
        self.lineCounter = len(self.code)
        self.filePath = filePath
    
    
    ''' Returns the indentation of the current line to be parsed - 
    pynta only has the normal indentations: 4, 8, 12, 16, 20... '''
    def indentationLevel(self, i):
        j = 0
        while self.code[i][j] == ' ':
            j+=1
        return j
            
            
    def parseMethod(self, methodRoot, begin, indentation):
        pass
     
    def parseClass(self, classRoot, begin, indentation):
        pass
    
    
    
    
    def parseCode(self):
        for i in range(0, self.lineCounter):
            wordList = self.code[i].split()

            # if empty line
            if(len(wordList) == 0 or self.indentationLevel(i) > 0):
                continue
            
            # if class 
            if(wordList[0] == 'class'):
                className = ''              
                for j in range(0, len(wordList[1])):
                    if wordList[1][j] == ':' or wordList[1][j] == '(':
                        break
                    className += wordList[1][j]
                newClass = Tree.SubElement(self.moduleRoot, 'Class', {'name' : className})
                self.parseClass(newClass, i, 4)
                    
            
            # if free method
            if(wordList[0] == 'def'):
                methodName = ''
                for j in range(0, len(wordList[1])):
                    if wordList[1][j] == ':' or wordList[1][j] == '(':
                        break
                    methodName += wordList[1][j]
                newMethod = Tree.SubElement(self.moduleRoot, 'FreeMethod', {'name' : methodName})
                self.parseMethod(newMethod, i, 4)
                
        