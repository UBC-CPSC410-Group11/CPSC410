'''
Created on Nov 20, 2013

@author: ericchu
'''
from CodeNeighbourhood.Analyzer.CustomTypes import Class
from CodeNeighbourhood.Analyzer.CustomTypes import Method
from CodeNeighbourhood.Analyzer.CustomTypes import Module
from CodeNeighbourhood.Analyzer.CustomTypes import Package
from CodeNeighbourhood.Analyzer.ScoreQuality import ScoreQuality
from CodeNeighbourhood.Analyzer.XMLParser import XMLParser
import unittest

''' Unit test class for the package Analyzer ''' 

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.aclass = Class("TheClassName",5,30)
        self.method = Method("TheMethodName",3,4,2,0)
        self.module = Module("TheModuleName")
        self.package = Package("ThePackageName")
        self.score = ScoreQuality()
        afile = open("TestXMLSample.xml", "r")
        self.xmlString = "".join(afile.readlines())
        afile.close()

    ''' *** CustomTypes Tests *** ''' 

    def testCTClassConstructor(self):
        self.failUnless(self.aclass.getName() == "TheClassName")
        self.failUnless(self.aclass.getWidth() == 5)
        self.failUnless(self.aclass.getLines() == 30)
        
    def testCTClassAddMethod(self):
        self.failUnless(self.aclass.getMethods() == [])
        self.aclass.addMethod("method1")
        self.failUnless(self.aclass.getMethods() == ["method1"])
        self.aclass.addMethod("method2")
        self.failUnless(self.aclass.getMethods() == ["method1", "method2"])
        
    def testCTClassAddOutCall(self):
        self.failUnless(self.aclass.getOutCalls() == [])
        self.aclass.addOutCall("caller0", "callee0")
        self.aclass.addOutCall("caller1", "callee1")
        self.aclass.addOutCall("caller2", "callee2")
        outcall0 = self.aclass.getOutCalls()[0]
        outcall1 = self.aclass.getOutCalls()[1]
        outcall2 = self.aclass.getOutCalls()[2]
        self.failUnless(outcall0.getCaller() == "caller0")
        self.failUnless(outcall0.getCallee() == "callee0")
        self.failUnless(outcall1.getCaller() == "caller1")
        self.failUnless(outcall1.getCallee() == "callee1")
        self.failUnless(outcall2.getCaller() == "caller2")
        self.failUnless(outcall2.getCallee() == "callee2")

    def testCTClassSetScore(self):
        self.failUnless(self.aclass.getScore() == 0)
        self.aclass.setScore(123)
        self.failUnless(self.aclass.getScore() == 123)
        
    def testCTMethodConstructor(self):
        self.failUnless(self.method.getName() == "TheMethodName")
        self.failUnless(self.method.getParameters() == 3)
        self.failUnless(self.method.getLines() == 4)
        self.failUnless(self.method.getComments() == 2)
        self.failUnless(self.method.getDocLines() == 0)
        
    def testCTMethodSetScore(self):
        self.failUnless(self.method.getScore() == 0)
        self.method.setScore(8)
        self.failUnless(self.method.getScore() == 8)

    def testCTModuleConstructor(self):
        self.failUnless(self.module.getName() == "TheModuleName")
    
    def testCTModuleAddFreeMethod(self):
        self.failUnless(self.module.getFreeMethods() == 0)
        self.module.addFreeMethod()
        self.failUnless(self.module.getFreeMethods() == 1)
        self.module.addFreeMethod()
        self.failUnless(self.module.getFreeMethods() == 2)
        
    def testCTModuleAddClass(self):
        self.failUnless(self.module.getClasses() == [])
        self.module.addClass(self.aclass)
        self.failUnless(not (self.module.getClasses() == []))
        self.failUnless(self.module.getClasses()[0].getName() == "TheClassName")
        self.module.addClass(Class("Class2",3,50))
        self.failUnless(self.module.getClasses()[1].getName() == "Class2")

    def testCTPackageConstructor(self):
        self.failUnless(self.package.getName() == "ThePackageName")
                
    def testCTPackageAddModule(self):
        self.failUnless(self.package.getModules() == [])
        self.package.addModule(self.module)
        self.failUnless(self.package.getModules()[0].getName() == "TheModuleName")


    ''' *** XMLParser Tests *** ''' 
        
    def testXMLParserParse(self):
        self.xmlparser = XMLParser(self.xmlString)
        xmlPackages = self.xmlparser.getPackages()
        package0 = xmlPackages[0]
        package1 = xmlPackages[1]
        self.failUnless(package0.getName() == "apps")
        self.failUnless(package1.getName() == "conf")
        
        moduleNames = []
        for module in package0.getModules():
            moduleNames.append(module.getName())
        self.failUnless(moduleNames == ["__init__.py", "base.py", "decorators.py", "generic.py", "simple.py"])
        
        classNames = []
        for aclass in package0.getModules()[1].getClasses():
            classNames.append(aclass.getName())
        self.failUnless(classNames == ["PyntaAppBase", "PyntaApp"])
        
        methodNames = []
        for method in package0.getModules()[1].getClasses()[1].getMethods():
            methodNames.append(method.getName())
        self.failUnless(methodNames == ["__init__","__call__","dispatch","init_session","save_session","app_by_url","get_context","get","post","head"])
        
    
    ''' *** CustomTypes Tests *** ''' 
        
    def testSQgetStandardDeviation(self):
        self.failUnless(self.score.getStandardDeviation([0]) == 0)
        self.failUnless(self.score.getStandardDeviation([2,2,2,2,2,2]) == 0)
        self.failUnless(round(self.score.getStandardDeviation([1,3,2,6,4])) == 4.0)
        
    def testSQgetMean(self):
        self.failUnless(self.score.getMean([0]) == 0)
        self.failUnless(self.score.getMean([5,5,5,5,5,5,5,5,5]) == 5)
        self.failUnless(self.score.getMean([5,3,9,12]) == 7.25)
        
    def testSQgetMedian(self):
        self.failUnless(self.score.getMedian([1,2,3,4]) == 2.5)
        self.failUnless(self.score.getMedian([1,2,3,32789754]) == 2.5)
        self.failUnless(self.score.getMedian([-5434321,2,3,32789754]) == 2.5)
        self.failUnless(self.score.getMedian([-2343243,2,3,544321,1000000000]) == 3)
        self.failUnless(self.score.getMedian([1,2,3,4,5]) == 3)
        self.failUnless(self.score.getMean([1,2,3]) == 2)
        
    def testSQhugeMethodScore(self):
        self.failUnless(self.score.hugeMethScore([100,300,200,231,50,124]) == 3)
        self.failUnless(self.score.hugeMethScore([100,300,200,400,50,124]) == 3)
        self.failUnless(self.score.hugeMethScore([100,300,200,401,50,124]) == 2)
        self.failUnless(self.score.hugeMethScore([100,300,200,500,50,124]) == 2)
        self.failUnless(self.score.hugeMethScore([100,300,200,700,50,124]) == 1)
        self.failUnless(self.score.hugeMethScore([100,300,200,601,50,124]) == 1)
        self.failUnless(self.score.hugeMethScore([10000,300,200,500,50,124]) == 0)
        self.failUnless(self.score.hugeMethScore([100,300,200,700,50,12411]) == 0)
        self.failUnless(self.score.hugeMethScore([100,700,200,1100,50,124]) == 0)
        
    #this tests scores applied to the sample xml input to ensure all score assignment are accurate
    def testScoreAssignments(self):
        self.xmlparser = XMLParser(self.xmlString)
        xmlPackages = self.xmlparser.getPackages()
        scores = ScoreQuality()
        scores.scorePackages(xmlPackages)
        
        classScores = []
        methodScores = []
        for package in xmlPackages:
            for module in package.getModules():
                for theClass in module.getClasses():
                    classScores.append(theClass.getScore())
                    for method in theClass.getMethods():
                        methodScores.append(method.getScore())
        
        self.failUnless(classScores == [6,7,8,8,6,8,5,7,8])
        self.failUnless(methodScores == [6,6,3,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,2,5])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()