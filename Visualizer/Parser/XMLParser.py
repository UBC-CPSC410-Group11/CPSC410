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
            for pkgNode in doc.getElementsByTagName("Package"):
                pkg = Package(pkgNode.getAttribute("name"))
                self.packages.append(pkg)
            
                if pkgNode.hasChildNodes():
                    
                    for modNode in pkgNode.getElementsByTagName("Module"):
                        mod = Module(modNode.getAttribute("name"))
                        pkg.addModule(mod)
                        
                        if modNode.hasChildNodes():
                            
                            for classNode in modNode.getElementsByTagName("Class"):
                                cl = Class(classNode.getAttribute("name"), 
                                           classNode.getAttribute("score"),
                                           classNode.getAttribute("width"),
                                           classNode.getAttribute("lines"))
                                if (classNode.hasChildNodes()):
                                    
                                    for methodNode in classNode.getElementsByTagName("Method"):
                                        meth = Method(methodNode.getAttribute("name"),
                                                      methodNode.getAttribute("score"),
                                                      methodNode.getAttribute("parameters"),
                                                      methodNode.getAttribute("lines"))
                                        cl.addMethod(meth)
                                    
                                    for methodNode in classNode.getElementsByTagName("Method"):
                                        cl.addOutCall(methodNode.getAttribute("name"))
                                        
                                mod.addClass(cl)
                        for classNode in modNode.getElementsByTagName("FreeMethod"):
                            mod.addFreeMethod()
        
    def getPackages(self):
        return self.packages
'''    
def main():
    parser = XMLParser("/Users/jonrl33/git/CPSC410/SampleInput.xml")
    pkgs = parser.getPackages()
    
    for p in pkgs:
        for m in p.getModules():
            for c in m.getClasses():
                for meth in c.getMethods():
                    print (m.getName(), c.getName(), meth.getName())
                
        
        
if __name__ == "__main__":
    main()
'''        
        