#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 09:55:29 2022

Wrapper to get both MaxOnset (with separate indication of syllable stress) 
and Alaska rule syllabifications of a sequence

@author: sarahharper
"""
phonemes = " AH0"
phoneTimes = [[0.7587, 0.8086]]
alg = "basic"

def syllWord(phonemes, phoneTimes, alg):
    import sys
    import os
    #import numpy as np
    
    os.chdir('/Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/Code/')
    
    project_home = '/Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/Code/syllabification_method1'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path
            
    from syllabification_method1 import syll1
    
    syllBasic = syll1(phonemes)
    
    from syllabification_method2 import syll2
    
    alaska, maxons = syll2(phonemes)
    
    syllInWord = len(syllBasic) #get number of syllables in word
    
    basicDict = {}
    alaskaDict = {}
    psBLen = 0
    psALen = 0
    
    for sl in range(syllInWord):
        #set up dict for maxons (basic) syllabification
        syllNum = "S" + str(sl + 1)
        syllStress= str(syllBasic[sl][0])
        syllBOns = syllBasic[sl][1]
        syllBNuc = syllBasic[sl][2]
        syllBCoda = syllBasic[sl][3]
        phnsB = syllBOns + syllBNuc + syllBCoda
        syllBType = "O" + str(len(syllBOns)) + "C" + str(len(syllBCoda))
        syllBPhns = "_".join(phnsB)
        
        #start procedure to get the times for onset/nucleus/coda start and end for maxons syllabification
        #syllMNuc = maxons[sl][1] #vowel arpabet with stress still indicated - necessary for string matching
        #syllBPhnsMatch = syllBOns + syllMNuc + syllBCoda
        syllPhnLen = len(phnsB)
        if syllNum == "S1":
            syllStartIdx = 0
        else:   
            syllStartIdx = psBLen #get initial index (this line) and # of entries for phones in this syllable
        syllEndIdx = syllStartIdx + syllPhnLen - 1
        onsLen = len(syllBOns)
        codaLen = len(syllBCoda)
        if onsLen > 0:
            onsStart = phoneTimes[syllStartIdx][0];
            onsEnd = phoneTimes[syllStartIdx + onsLen - 1][1]
            nucStart = phoneTimes[syllStartIdx + onsLen][0]
            nucEnd = phoneTimes[syllStartIdx + onsLen][1]
        else:
            onsStart = []
            onsEnd = []
            nucStart = phoneTimes[syllStartIdx][0]
            nucEnd = phoneTimes[syllStartIdx][1]
        if codaLen > 0:
            codaStart = phoneTimes[syllEndIdx - codaLen + 1][0]
            codaEnd = phoneTimes[syllEndIdx][1]
        else:
            codaStart = []
            codaEnd = []
            
        basicDict[syllBPhns] = {'snum': syllNum, 'sstress': syllStress, 'stype': syllBType,
                               'parts': {'ons': syllBOns, 'nuc': syllBNuc, 'coda': syllBCoda},
                               'onsTimes': [onsStart, onsEnd], 'nucTimes': [nucStart, nucEnd], 'codaTimes': [codaStart, codaEnd]}
        psBLen = len(phnsB)
        
        #set up dict for alaska rule syllabification
        syllAOns = alaska[sl][0]
        syllACoda = alaska[sl][2]
        phnsA = syllAOns + syllBNuc + syllACoda
        syllAType = "O" + str(len(syllAOns)) + "C" + str(len(syllACoda))
        syllAPhns = "_".join(phnsA)
        
        #start procedure to get the times for onset/nucleus/coda start and end for maxons syllabification
        #syllAPhnsMatch = syllAOns + syllMNuc + syllACoda
        syllPhnLen = len(phnsA)
        if syllNum == "S1":
            syllStartIdx = 0
        else:
            syllStartIdx = psALen
        #syllAPhnsMatch = " ".join(syllAPhnsMatch)
        syllEndIdx = syllStartIdx + syllPhnLen - 1
        onsLen = len(syllAOns)
        codaLen = len(syllACoda)
        if onsLen > 0:
            onsStart = phoneTimes[syllStartIdx][0];
            onsEnd = phoneTimes[syllStartIdx + onsLen - 1][1]
            nucStart = phoneTimes[syllStartIdx + onsLen][0]
            nucEnd = phoneTimes[syllStartIdx + onsLen][1]
        else:
            onsStart = []
            onsEnd = []
            nucStart = phoneTimes[syllStartIdx][0]
            nucEnd = phoneTimes[syllStartIdx][1]
        if codaLen > 0:
            codaStart = phoneTimes[syllEndIdx - codaLen + 1][0]
            codaEnd = phoneTimes[syllEndIdx][1]
        else:
            codaStart = []
            codaEnd = []
            
        alaskaDict[syllAPhns] = {'snum': syllNum, 'sstress': syllStress, 'stype': syllAType,
                               'parts': {'ons': syllAOns, 'nuc': syllBNuc, 'coda': syllACoda},
                               'onsTimes': [onsStart, onsEnd], 'nucTimes': [nucStart, nucEnd], 'codaTimes': [codaStart, codaEnd]}
        psALen = len(phnsA)
        
    if alg == "alaska":
        outsyll = alaskaDict
    else:
        outsyll = basicDict
    
    return outsyll
    

b = syllWord(phonemes, phoneTimes, alg)


#consider adding another input to script that has time stamps for each phoneme -- then can add those times easily here instead of having to port back to matlab
#and then get times for onset/coda/nucleus onset and offset