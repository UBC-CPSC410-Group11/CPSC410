 
'''
Created on 2013-10-22

@author: jonrl33
'''

class Class(object):
    name = ""
    methods = []
    outCalls = []
    score = ""
    lines = ""
    
    # Creates a new Class instance with name and lines    
    def __init__(self, in_Name, in_Lines):
        self.methods = []
        self.outCalls = []
        self.name = in_Name
        self.score = 0
        self.lines = in_Lines
    
    # Adds Method instance to list of Methods
    def addMethod(self, in_Method):
        self.methods.append(in_Method)
    
    # Adds unique OutCall instance to list of OutCalls
    # Or, if a duplicate, increments the count value of the OutCall    
    def addOutCall(self, in_Caller, in_Callee, in_Count):
        for outCall in self.outCalls:
            if ((outCall.getCaller() == in_Caller) and (outCall.getCallee() == in_Callee)):
                outCall.addCall()
                return
        self.outCalls.append(OutCall(in_Caller, in_Callee, in_Count))
        
    # Returns the list of OutCalls
    def getOutCalls(self):
        return self.outCalls
    
    # Returns the list of Methods    
    def getMethods(self):
        return self.methods
    
    # Returns the Class name
    def getName(self):
        return self.name
    
    # Returns the Class score (Integer from 0 to 9)
    def getScore(self):
        return self.score
    
    # Sets the Class score (Integer from 0 to 9)
    def setScore(self, in_Score):
        self.score = in_Score
        
    # Returns the number of lines (Integer)
    def getLines(self):
        return self.lines
    
class Method(object):
    name = ""
    score = ""
    parameters = ""
    lines = ""
    commentLines = ""
    documentationLines = ""
    
    # Creates a new Method instance with the name and numbers of parameters, lines, comment lines,
    # and documentation lines
    def __init__(self, in_Name, in_Parameters, in_Lines, in_ComLines, in_DocLines):
        self.name = in_Name
        self.score = 0
        self.parameters = in_Parameters
        self.lines = in_Lines
        self.commentLines = in_ComLines
        self.documentationLines = in_DocLines
    
    # Returns the name of the Method
    def getName(self):
        return self.name
    
    # Returns the Method score
    def getScore(self):
        return self.score
    
    # Returns the number of parameters (Integer)
    def getParameters(self):
        return self.parameters
    
    # Returns the number of lines (Integer)
    def getLines(self):
        return self.lines
    
    # Sets the Method score (Integer from 0 to 9)
    def setScore(self, in_Score):
        self.score = in_Score
    
    # Returns the number of comments (Integer)
    def getComments(self):
        return self.commentLines
    
    # Returns the number of lines of documentation (Integer)
    def getDocLines(self):
        return self.documentationLines


class Module(object):
    name = ""
    classes = []
    freeMethods = 0
    
    # Creates an Module instance with the given name
    def __init__(self, in_Name):
        self.name = in_Name
        self.classes = []
        self.freeMethods = 0
    
    # Adds a Class Instance to the list of Classes    
    def addClass(self, in_Class):
        self.classes.append(in_Class)
    
    # Increments the counter of number of free methods
    def addFreeMethod(self):
        self.freeMethods = self.freeMethods + 1
    
    # Returns the list of Classes
    def getClasses(self):
        return self.classes
    
    # Returns the number of free methods (Integer)
    def getFreeMethods(self):
        return self.freeMethods
    
    # Returns the Module name
    def getName(self):
        return self.name

class Package(object):
    name = ""
    modules = []
    
    # Creates a Package instance with the given name
    def __init__(self, in_Name):
        self.name = in_Name
        self.modules = []
    
    # Adds a Module instance to the list of Modules    
    def addModule(self, in_Module):
        self.modules.append(in_Module)
    
    # Returns the list of Modules
    def getModules(self):
        return self.modules
    
    # Returns the Package name
    def getName(self):
        return self.name
    
class OutCall(object):
    caller = ""
    callee = ""
    numCalls = ""
    inModuleCall = ""
    
    # Creates an OutCall instance with caller, callee and the number of calls
    def __init__(self, in_Caller, in_Callee, in_Count):
        self.caller = in_Caller
        self.callee = in_Callee
        self.numCalls = in_Count
        self.inModuleCall = ""
    
    # Increments the number of calls    
    def addCall(self):
        self.numCalls = self.numCalls + 1
    
    # Returns the number of calls
    def getNumCalls(self):
        return self.numCalls
    
    # Returns the caller Class name
    def getCaller(self):
        return self.caller
    
    # Returns the callee Class name
    def getCallee(self):
        return self.callee
    
    # Returns a boolean if OutCall is within a Module (True) otherwise False
    def withinModule(self):
        return self.inModuleCall
    
    # Sets inModule boolean value
    def setInModule(self, in_Bool):
        self.inModuleCall = in_Bool

# Accepts a list of Packages and sets the inModule value for each OutCall in each Class
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

# Returns true if in_ClassName is present in the in_Classes list of Class names                
def containsClassName(in_ClassName, in_Classes):
    for cls in in_Classes:
        if (in_ClassName == cls.getName()):
            return True
    return False
