'''
Created on 21.10.2013

@author: Chris
'''

import xml.etree.cElementTree as Tree


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
    
    ''' Returns True if line is empty or False if line is not empty '''
    def isEmpty(self, i):
        if(len(self.code[i]) <= 1):
            return True
        for j in range(0, len(self.code[i])):
            if(self.code[i][j] != ' ' or self.code[i][j] != '\n'):
                return False
        return True
        
    
    
    ''' Returns if the indentation of the current line to be parsed is still as deep
        as the current depth we are on '''
    def indentationLevel(self, i, indentation):
        if (self.isEmpty(i)):
            return True
        j = 0
        while self.code[i][j] == ' ':
            j+=1
        if j >= indentation:
            return True
        else:
            return False
    
    
    
    ''' Goes through all the lines of a free method, but does nothing -
        maybe needed later '''        
    def parseFreeMethod(self, methodRoot, begin, indentation):
        while (begin < self.lineCounter and (self.indentationLevel(begin, indentation))):
            begin += 1
        return begin-1
        
        
    ''' Count lines from self.code between indices [begin, end[ '''
    def countLines(self, begin, end):
        return 11
    
    
    
    ''' Count comments from self.code between indices [begin, end[ '''
    def countComments(self, begin, end):
        return 12
    
    
    
    ''' Find calls to other classes in a method between indices [begin, end[ '''
    def findOutcalls(self, begin, end): 
        pass
    
    
    
    ''' Calculate score of method or class between indices [begin, end[ -
        (probably two different methods needed) '''
    def calculateScore(self, begin, end):
        return 10   
    
    
    
    ''' Iterate through lines to find end of method and then parse it '''
    def parseMethod(self, methodRoot, begin, indentation):
        pass
     
    
    
    ''' Iterate through lines to find end of class and then parse it '''
    def parseClass(self, classRoot, begin, indentation):
        i = 0
        while (self.indentationLevel(begin + i, indentation)):
            i += 1
            if(begin+i >= self.lineCounter):
                break
        end = begin + i
        
        lines = self.countLines(begin, end)
        score = self.calculateScore(begin, end)
        
        classRoot.set('lines', str(lines))
        classRoot.set('score', str(score))
        
        # TODO:   iterate from begin to end again (I know, probably not really efficient, but easier)
        #         and look for methods or nested classes, then call parseMethod() or parseClass() again

        return end - 1
    
    
    
    ''' Goes through all the lines and divides the program code 
    into classes and free methods '''
    def parseCode(self):
        for i in range(0, self.lineCounter):
            # parse line
            wordList = self.code[i].split()

            # if empty line or more indented than base level 0
            if(self.isEmpty(i) or not (self.indentationLevel(i, 0) and not self.indentationLevel(i, 4))):
                continue
            
            # if line is class declaration
            if(wordList[0] == 'class'):
                className = ''              
                for j in range(0, len(wordList[1])):
                    if wordList[1][j] == ':' or wordList[1][j] == '(':
                        break
                    className += wordList[1][j]
                newClass = Tree.SubElement(self.moduleRoot, 'Class', {'name' : className})
                self.parseClass(newClass, i+1, 4)
                    
            
            # if line is free method declaration
            if(wordList[0] == 'def'):
                methodName = ''
                for j in range(0, len(wordList[1])):
                    if wordList[1][j] == ':' or wordList[1][j] == '(':
                        break
                    methodName += wordList[1][j]
                newMethod = Tree.SubElement(self.moduleRoot, 'FreeMethod', {'name' : methodName})
                i = self.parseFreeMethod(newMethod, i+1, 4)
                
        