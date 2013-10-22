'''
Created on 2013-10-22

@author: jonrl33
'''
from xml.dom.minidom import parse
from CustomTypes import Package, Module, Class, Method

class XMLParser(object):
    packages = []
    
    def __init__(self, in_File):
        self.parseFile(in_File)
            
    def parseFile(self, in_File):
        doc = parse(in_File)
        if doc.hasChildNodes():
            for pkgNode in doc.childNodes:
                pkg = Package(pkgNode.attributes["name"].value)
            
                if pkgNode.hasChildNodes():
                    for modNode in pkgNode.childNodes:
                        mod = Module(modNode.attributes["name"].value)
                        pkg.addModule(mod)
                
                    if modNode.hasChildNodes():
                        for classNode in modNode:
                            if (classNode.tagName == "Class"):
                                cl = Class(classNode.attributes["name"].value, 
                                           classNode.attributes["score"].value,
                                           classNode.attributes["width"].value,
                                           classNode.attributes["lines"].value)
                                mod.addClass(cl)
                                if classNode.hasChildNodes():
                                    for methodNode in classNode.childNodes:
                                        if (methodNode.tagName == "Method"):
                                            meth = Method(methodNode.attributes["name"].value,
                                                          methodNode.attributes["score"].value,
                                                          methodNode.attributes["parameters"].value,
                                                          methodNode.attributes["lines"].value)
                                            cl.addMethod(meth)
                                        elif (methodNode.tagName == "OutCall"):
                                            cl.addOutCall(methodNode.attributes["name"].value)
                            elif (classNode.tagName == "FreeMethod"):
                                mod.addFreeMethod()
        
    def getPackages(self):
        return self.packages