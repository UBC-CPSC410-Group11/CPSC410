'''
Created on 2013-11-15

@author: jonrl33
'''
from CustomTypes import *

class ScoreQuality(object):
    '''
    classdocs
    '''

    def __init__(self):
        pass
    
    # Accepts a list of Packages
    # Calls scoreMod on each Module in the Package
    def scorePackages(self, pkgs):
        for pkg in pkgs:
            for mod in pkg.getModules():
                self.scoreMod(mod)
                
    # accepts a Module
    # calls scoreClass on each Class in the Module        
    def scoreMod(self, mod):
        for cls in mod.getClasses():
            self.scoreClass(cls)
    
    # Accepts a Class
    # Calls scoreMethod on each method in the class
    # Sets the score parameter for the class based on the scores of its methods,
    # the number of out-of-module method calls, and method length:
    # if there are more than 2 methods, the variance between method lengths is analyzed.
    # if there are 2 or less methods, the presence of long methods is analyzed.
    def scoreClass(self, cls):
        for meth in cls.getMethods():
            self.scoreMethod(meth)
        score = self.avgMethScore(cls.getMethods()) + self.outcallScore(cls.getOutCalls())
        lengths = []
        for meth in cls.getMethods():
            lengths.append(int(meth.getLines()))
        
        if (len(cls.getMethods()) > 2):
            score = score + self.mLengthVarianceScore(lengths)
        else:
            score = score + self.hugeMethScore(lengths)
        cls.setScore(score)
    
    # Accepts a Method
    # Scores the method by calling scoreMethodComments to analyze commenting, by analyzing
    # the presence of documentation above the method definition, and by analyzing the number
    # of parameters.
    def scoreMethod(self, meth):
        score = 0;
        if (int(meth.getDocLines()) > 0):
            score = score + 3
            
        score = score + self.scoreMethComments(meth)
        mParams = int(meth.getParameters())
        paramScore = 0
        
        if (mParams <= 2):
            paramScore = 4
        elif(mParams <= 3):
            paramScore = 2
        elif(mParams <= 4):
            paramScore = 1
        else: 
            paramScore = 0
        score = score + paramScore        
        meth.setScore(score)
        
    # Accepts a Method
    # Returns an integer score from 0 to 3 based on the percent of lines that are comments    
    def scoreMethComments(self, meth):
        coms = meth.getComments()
        mLines = meth.getLines()
        percent = int(float(100*coms)/int(mLines))
        score = 0
        if (percent == 0):
            score = 2
        elif (percent <= 10):
            score = 1
        elif (percent <= 20):
            score = 0
        return score
    
    # Accepts a list of Methods
    # Returns a float of the average score of the methods
    def avgMethScore(self, meths):
        if (len(meths) == 0):
            return 0
        total = 0
        for meth in meths:
            total = total + int(meth.getScore())
        avg = total/(float(len(meths)))
        score = 3*(avg/9)
        if (score - int(score) < 0.5):
            score = int(score)
        else:
            score = int(score) + 1
        return score

    
    # Accepts a list of OutCalls
    # Returns an integer score from 0 to 3 based on the number of out-of-module Class references
    # If a specific class is referenced more than 5 times, that OutCall is deemed excessive
    # Each excessive OutCall reduces the score by 1 point to a minimum of 0
    def outcallScore(self, outcalls):
        excessiveCalls = 0
        
        for out in outcalls:
            if ((out.withinModule() == False) and (out.getNumCalls() >= 4)):
                excessiveCalls = excessiveCalls + 1
        score = 0
        if (excessiveCalls == 0):
            score = 1
        elif (excessiveCalls > 0): 
            score = 0
        return score
    
    # Accepts a list of Method length integers
    # Returns an integer score from 0 to 3 based on length of the longest method
    # Method lengths > 1000 receive 0; >600 receive 1, >400 receive 2, otherwise 3
    def hugeMethScore(self, lengths):
        biggest = 0
        for length in lengths:
            if (length > biggest):
                biggest = length
        if (biggest > 500):
            return 0
        elif (biggest > 300):
            return 2
        elif (biggest > 200):
            return 3
        elif (biggest > 100):
            return 4
        else:
            return 5
                
    # Accepts a list of integers of Method lengths
    # returns an integer score from 0 to 3 based on the skew of method lengths    
    def mLengthVarianceScore(self, lengths):
        median = self.getMedian(lengths)    
        mean = self.getMean(lengths)    
        sd = self.getStandardDeviation(lengths)
        skew = float(mean - float(median))/sd
        
        score = 0
        if (-0.05 <= skew <= 0.05):
            score = 5
        elif (-0.1 <= skew <= 0.1):
            score = 4
        elif (-0.2 <= skew <= 0.2):
            score = 2
        elif (-0.3 <= skew <= 0.3):
            score = 1
        return score
    
    # Accepts a list of integers of Method lengths
    # Returns a float of the median of the list    
    def getMedian(self, in_Lengths):
        sList = sorted(in_Lengths)
        med = 0
        if (len(sList) % 2 == 1):
            med = sList[(len(sList) + 1 ) / 2 - 1]
        else:
            mHigh = sList[len(sList)/2]
            mLow = sList[len(sList)/2 - 1]
            med = float(mHigh + mLow) / 2
        return med
    
    # Accepts a list of integers of Method lengths
    # Returns a float of the mean of the list
    def getMean(self, in_Lengths):
        mean = 0
        for val in in_Lengths:
            mean = mean + int(val)
        mean = mean/float(len(in_Lengths))
        return mean
    
    # Accepts a list of integers of Method lengths
    # Returns a float of the standard deviation of the list
    def getStandardDeviation(self, in_Lengths):
        variance = 0
        mean = self.getMean(in_Lengths)
        for val in in_Lengths:
            variance = variance + float(mean - int(val))**2            
        sd = variance**(0.5)
        return sd