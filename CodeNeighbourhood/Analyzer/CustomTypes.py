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
    
    def __init__(self, in_Name, in_Width, in_Lines):
        self.methods = []
        self.outCalls = []
        self.name = in_Name
        self.score = 0
        self.width = in_Width
        self.lines = in_Lines

    def addMethod(self, in_Method):
        self.methods.append(in_Method)
        
    def addOutCall(self, in_Caller, in_Callee):
        for outCall in self.outCalls:
            if ((outCall.getCaller() == in_Caller) and (outCall.getCallee() == in_Callee)):
                outCall.addCall()
                return
        self.outCalls.append(OutCall(in_Caller, in_Callee))
        
    
    def getOutCalls(self):
        return self.outCalls
        
    def getMethods(self):
        return self.methods
    
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def setScore(self, in_Score):
        self.score = in_Score
    
    def getWidth(self):
        return self.width
    
    def getLines(self):
        return self.lines
    
class Method(object):
    name = ""
    score = ""
    parameters = ""
    lines = ""
    commentLines = ""
    documentationLines = ""
    def __init__(self, in_Name, in_Parameters, in_Lines, in_ComLines, in_DocLines):
        self.name = in_Name
        self.score = 0
        self.parameters = in_Parameters
        self.lines = in_Lines
        self.commentLines = in_ComLines
        self.documentationLines = in_DocLines
    
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def getParameters(self):
        return self.parameters
    
    def getLines(self):
        return self.lines
    
    def setScore(self, in_Score):
        self.score = in_Score
    


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
    
class OutCall(object):
    caller = ""
    callee = ""
    numCalls = ""
    inModuleCall = ""
    
    def __init__(self, in_Caller, in_Callee):
        self.caller = in_Caller
        self.callee = in_Callee
        self.numCalls = 1
        self.inModuleCall = ""
        
    def addCall(self):
        self.numCalls = self.numCalls + 1

    def getNumCalls(self):
        return self.numCalls
    
    def getCaller(self):
        return self.caller
    
    def getCallee(self):
        return self.callee
    
    def withinModule(self):
        return self.inModuleCall
    
    def setInModule(self, in_Bool):
        self.inModuleCall = in_Bool

def setInModuleBools(in_Packages):
    outs = []
    for pack in in_Packages:
        for mod in pack.getModules():
            for cl in mod.getClasses():
                for out in cl.getOutCalls():
                    if (containsClassName(out.getCallee(), mod.getClasses())):
                        out.setInModule(True)
                    else:
                        out.setInModule(False)
                    outs.append(out)
    return outs
                
def containsClassName(in_ClassName, in_Classes):
    for cls in in_Classes:
        if (in_ClassName == cls.getName()):
            return True
    return False
