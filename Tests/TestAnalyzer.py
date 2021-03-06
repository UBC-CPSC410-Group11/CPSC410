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

    ''' constructs necessary objects for test to proceed properly, also reads sample XML 
    input into a string in preparation for tests that require XML input '''
    def setUp(self):
        self.aclass = Class("TheClassName",30)
        self.method = Method("TheMethodName",3,4,2,0)
        self.module = Module("TheModuleName")
        self.package = Package("ThePackageName")
        self.score = ScoreQuality()
        afile = open("TestXMLSample.xml", "r")
        self.xmlString = "".join(afile.readlines())
        afile.close()


    ''' *** CustomTypes Tests *** ''' 

    ''' Calls get methods in CustomTypes::Class to verify that self.aclass has been properly constructed in setUp '''    
    def testCTClassConstructor(self):
        self.failUnless(self.aclass.getName() == "TheClassName")
        self.failUnless(self.aclass.getLines() == 30)
        
    ''' call add and get methods to verify that method adder and setter functions in CustomTypes::Class work properly'''    
    def testCTClassAddMethod(self):
        self.failUnless(self.aclass.getMethods() == [])
        self.aclass.addMethod("method1")
        self.failUnless(self.aclass.getMethods() == ["method1"])
        self.aclass.addMethod("method2")
        self.failUnless(self.aclass.getMethods() == ["method1", "method2"])
     
    ''' call add and get Outcalls to verify that Outcalls can be constructed and added to class properly'''    
    def testCTClassAddOutCall(self):
        self.failUnless(self.aclass.getOutCalls() == [])
        self.aclass.addOutCall("caller0", "callee0",6)
        self.aclass.addOutCall("caller1", "callee1",4)
        self.aclass.addOutCall("caller2", "callee2",5)
        outcall0 = self.aclass.getOutCalls()[0]
        outcall1 = self.aclass.getOutCalls()[1]
        outcall2 = self.aclass.getOutCalls()[2]
        self.failUnless(outcall0.getCaller() == "caller0")
        self.failUnless(outcall0.getCallee() == "callee0")
        self.failUnless(outcall1.getCaller() == "caller1")
        self.failUnless(outcall1.getCallee() == "callee1")
        self.failUnless(outcall2.getCaller() == "caller2")
        self.failUnless(outcall2.getCallee() == "callee2")

    ''' call score setter and getter to ensure that scores can be set in classes properly '''
    def testCTClassSetScore(self):
        self.failUnless(self.aclass.getScore() == 0)
        self.aclass.setScore(123)
        self.failUnless(self.aclass.getScore() == 123)
        
    ''' Calls get methods in CustomTypes::Method to verify that self.method has been properly constructed in setUp '''    
    def testCTMethodConstructor(self):
        self.failUnless(self.method.getName() == "TheMethodName")
        self.failUnless(self.method.getParameters() == 3)
        self.failUnless(self.method.getLines() == 4)
        self.failUnless(self.method.getComments() == 2)
        self.failUnless(self.method.getDocLines() == 0)
    
    ''' call score setter and getter to ensure that scores can be set in methods properly '''
    def testCTMethodSetScore(self):
        self.failUnless(self.method.getScore() == 0)
        self.method.setScore(8)
        self.failUnless(self.method.getScore() == 8)

    ''' call get methods in CustomTypes::Module to verify that self.module has been properly constructed in setUp '''    
    def testCTModuleConstructor(self):
        self.failUnless(self.module.getName() == "TheModuleName")
    
    ''' call free method getter and setters to ensure that free methods can be added to modules properly '''    
    def testCTModuleAddFreeMethod(self):
        self.failUnless(self.module.getFreeMethods() == 0)
        self.module.addFreeMethod()
        self.failUnless(self.module.getFreeMethods() == 1)
        self.module.addFreeMethod()
        self.failUnless(self.module.getFreeMethods() == 2)
        
    ''' call add and get class to ensure that classes can be added to modules properly '''
    def testCTModuleAddClass(self):
        self.failUnless(self.module.getClasses() == [])
        self.module.addClass(self.aclass)
        self.failUnless(not (self.module.getClasses() == []))
        self.failUnless(self.module.getClasses()[0].getName() == "TheClassName")
        self.module.addClass(Class("Class2",50))
        self.failUnless(self.module.getClasses()[1].getName() == "Class2")

    ''' Calls get methods in CustomTypes::Package to verify that self.package has been properly constructed in setUp '''    
    def testCTPackageConstructor(self):
        self.failUnless(self.package.getName() == "ThePackageName")
       
    ''' Calls module adder and getter to ensure that modules can be added to packages properly '''             
    def testCTPackageAddModule(self):
        self.failUnless(self.package.getModules() == [])
        self.package.addModule(self.module)
        self.failUnless(self.package.getModules()[0].getName() == "TheModuleName")


    ''' *** XMLParser Tests *** ''' 
        
    ''' tests Analyzer::XMLParser::XMLParser by using a sample XML input and solicit expected results from parser
        (verify information contained in module, class, and method objects) '''
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
        
    
    ''' *** ScoreQuality Tests *** ''' 
      
    ''' tests standard deviation calculation in ScoreQuality::ScoreQuality '''    
    def testSQgetStandardDeviation(self):
        self.failUnless(self.score.getStandardDeviation([0]) == 0)
        self.failUnless(self.score.getStandardDeviation([2,2,2,2,2,2]) == 0)
        self.failUnless(round(self.score.getStandardDeviation([1,3,2,6,4])) == 4.0)
        
    ''' tests mean calculation in ScoreQuality::ScoreQuality '''    
    def testSQgetMean(self):
        self.failUnless(self.score.getMean([0]) == 0)
        self.failUnless(self.score.getMean([5,5,5,5,5,5,5,5,5]) == 5)
        self.failUnless(self.score.getMean([5,3,9,12]) == 7.25)
        
    ''' tests median calculation in ScoreQuality::ScoreQuality '''
    def testSQgetMedian(self):
        self.failUnless(self.score.getMedian([1,2,3,4]) == 2.5)
        self.failUnless(self.score.getMedian([1,2,3,32789754]) == 2.5)
        self.failUnless(self.score.getMedian([-5434321,2,3,32789754]) == 2.5)
        self.failUnless(self.score.getMedian([-2343243,2,3,544321,1000000000]) == 3)
        self.failUnless(self.score.getMedian([1,2,3,4,5]) == 3)
        self.failUnless(self.score.getMean([1,2,3]) == 2)
        
    ''' tests score assignment according to method size in ScoreQuality::ScoreQuality '''
    def testSQhugeMethodScore(self):
        self.failUnless(self.score.hugeMethScore([100,300,200,231,50,124]) == 3)
        self.failUnless(self.score.hugeMethScore([100,300,200,400,50,124]) == 2)
        self.failUnless(self.score.hugeMethScore([100,300,200,401,50,124]) == 2)
        self.failUnless(self.score.hugeMethScore([100,300,200,500,50,124]) == 2)
        self.failUnless(self.score.hugeMethScore([100,300,200,700,50,124]) == 0)
        self.failUnless(self.score.hugeMethScore([100,300,200,601,50,124]) == 0)
        self.failUnless(self.score.hugeMethScore([10000,300,200,500,50,124]) == 0)
        self.failUnless(self.score.hugeMethScore([100,300,200,700,50,12411]) == 0)
        self.failUnless(self.score.hugeMethScore([100,700,200,1100,50,124]) == 0)
        
    ''' tests scores applied to the sample xml input to ensure all score assignment are accurate '''
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
        
        self.failUnless(classScores == [6, 5, 8, 8, 6, 8, 3, 7, 8])
        self.failUnless(methodScores == [6, 6, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 2, 5])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()