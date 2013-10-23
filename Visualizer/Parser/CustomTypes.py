'''
Created on 2013-10-22

@author: jonrl33
'''
class Class(object):
    name = ""
    methods = []
    outCalls = []
    score = ""
    width = ""
    lines = ""
    
    def __init__(self, in_Name, in_Score, in_Width, in_Lines):
        self.methods = []
        self.outCalls = []
        self.name = in_Name
        self.score = in_Score
        self.width = in_Width
        self.lines = in_Lines

    def addMethod(self, in_Method):
        self.methods.append(in_Method)
        
    def addOutCall(self, in_ClassName):
        self.outCalls.append(in_ClassName)
    
    def getOutCalls(self):
        return self.outCalls
        
    def getMethods(self):
        return self.methods
    
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def getWidth(self):
        return self.width
    
    def getLines(self):
        return self.lines
    
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
        self.classes = []
        self.freeMethods = 0
        
    def addClass(self, in_Class):
        self.classes.append(in_Class)
    
    def addFreeMethod(self):
        self.freeMethods = self.freeMethods + 1
    
    def getClasses(self):
        return self.classes
    
    def getFreeMethods(self):
        return self.freeMethods
    
    def getName(self):
        return self.name

class Package(object):
    name = ""
    modules = []
    
    def __init__(self, in_Name):
        self.name = in_Name
        self.modules = []
        
    def addModule(self, in_Module):
        self.modules.append(in_Module)
    
    def getModules(self):
        return self.modules
    
    def getName(self):
        return self.name
