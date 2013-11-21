'''
Created on 2013-10-22

@author: jonrl33
'''
from xml.dom.minidom import parseString
from CustomTypes import Package, Module, Class, Method

class XMLParser(object):
    packages = []
    def __init__(self, in_File):
        self.parseFile(in_File)
    
    # Given an XMLString from the SourceParser, parses the string and populates self.packages
    # with corresponding Modules, Classes, Methods, and OutCalls to the given input        
    def parseFile(self, in_String):
        doc = parseString(in_String)
        if doc.hasChildNodes():
            for pkgNode in doc.getElementsByTagName("Package"):
                pkg = Package(pkgNode.getAttribute("name"))
                self.packages.append(pkg)
            
                if pkgNode.hasChildNodes():
                    
                    for modNode in pkgNode.getElementsByTagName("Module"):
                        mod = Module(modNode.getAttribute("name"))
                        pkg.addModule(mod)
                        
                        if modNode.hasChildNodes():
                            
                            for classNode in modNode.getElementsByTagName("Class"):
                                className = classNode.getAttribute("name")
                                classLines = classNode.getAttribute("lines")
                                cl = Class(className, classLines)
                                if (classNode.hasChildNodes()):
                                    
                                    for methodNode in classNode.getElementsByTagName("Method"):
                                        mName = methodNode.getAttribute("name")
                                        mParam = methodNode.getAttribute("parameters")
                                        mLines = methodNode.getAttribute("lines")
                                        mComLines = methodNode.getAttribute("comments")
                                        mDocLines = methodNode.getAttribute("documentation")
                                        meth = Method(mName, mParam, mLines, mComLines, mDocLines)
                                        cl.addMethod(meth)
                                    
                                    for outCallNode in classNode.getElementsByTagName("OutCall"):
                                        for outCall in outCallNode.getElementsByTagName("ClassName"):
                                            cl.addOutCall(cl.getName(), outCall.getAttribute("name"), outCall.getAttribute("count"))
                                        
                                mod.addClass(cl)
                        for classNode in modNode.getElementsByTagName("FreeMethod"):
                            mod.addFreeMethod()
    # Returns the list of Packages    
    def getPackages(self):
        return self.packages
'''    
def main():
    parser = XMLParser("/Users/jonrl33/git/CPSC410/SampleInput.xml")
    pkgs = parser.getPackages()
    setInModuleBools(pkgs)
    
    for p in pkgs:
        for m in p.getModules():
            for c in m.getClasses():
                #for meth in c.getMethods():
                #    print (m.getName(), c.getName(), meth.getName())
                for out in c.getOutCalls():
                    print(out.getCaller(), out.getCallee(), out.withinModule())
                
       
        
if __name__ == "__main__":
    main()
'''       
        