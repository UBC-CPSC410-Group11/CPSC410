'''
Created on 2013-10-22

@author: jonrl33
'''
class Class(object):
    name = ""
    methods = []
    outCalls = []
    
    def __init__(self, in_Name, in_Package, in_Module):
        self.name = in_Name
        self.package = in_Package
        self.module = in_Module
        

    def addMethod(self, in_Method):
        self.methods.append(in_Method)
        
    def addOutCall(self, in_ClassName):
        self.outCalls.append(in_ClassName)
    
    def getOutCalls(self):
        return self.outCalls
        
    def getMethods(self):
        return self.methods
    
class Method(object):
    name = ""
    score = ""
    parameters = ""
    lines = ""
    def __init__(self, in_Name, in_Score, in_Parameters, in_Lines):
        self.name = in_Name
        self.score = in_Score
        self.parameters = in_Parameters
        self.lines = in_Lines
    
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def getParameters(self):
        return self.parameters
    
    def getLines(self):
        return self.lines
    


class Module(object):
    name = ""
    classes = []
    freeMethods = 0
    
    def __init__(self, in_Name):
        self.name = in_Name
        
    def addClass(self, in_Class):
        self.classes.append(in_Class)
    
    def addFreeMethod(self):
        self.freeMethods = self.freeMethods + 1
    
    def getClasses(self):
        return self.classes
    
    def getFreeMethods(self):
        return self.freeMethods

class Package(object):
    name = ""
    modules = []
    
    def __init__(self, in_Name):
        self.name = in_Name
        
    def addModule(self, in_Module):
        self.modules.append(in_Module)
    
    def getModules(self):
        return self.modules
