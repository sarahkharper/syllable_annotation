#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:06:48 2022

@author: sarahharper
"""

import os
import pandas as pd
#import numpy as np
#import parselmouth
#from parselmouth.praat import call
import tgt
#import statistics
import glob
import pickle

#define the speaker and block being analyzed, and base directory for analysis
spkr = ""
blk = ""
dirName = ''

#open pickle with part of syllable definition dict for all words in task
os.chdir(dirName)
stimDct = pickle.load(open("syll_bound_pos.pkl", "rb"))

#make list of key names in wrdDct

timedata = []
segdata = []

#iterate through all checked TextGrids in block
os.chdir(dirName + "/Data/" + spkr + "/" + blk + "/phones/results/speaker1")
for txtgrd in glob.glob("*.TextGrid"):
    print("Processing {}...".format(txtgrd))
    t = tgt.read_textgrid(txtgrd)
    phone_tier = t.get_tier_by_name('phones')
    word_tier = t.get_tier_by_name('words')
    for w in range(0, len(word_tier)):  #iterate through labeled words in TextGrid
        wrdInt = word_tier[w]
        wrd = wrdInt.text #get word
        wrdStart = wrdInt.start_time #get interval start time
        wrdEnd = wrdInt.end_time #get interval end time
        phns = phone_tier.get_annotations_between_timepoints(wrdStart, wrdEnd)
        
        #get part of syllable info for current word
        stimPOS = stimDct[wrd]
        o1 = []
        c1 = []
        c2 = []
        nInd = []
        nucleus = stimPOS['S1']['n'] #get identity of nucelus vowel
        for x in range(0, len(phns)): #get vowel end time (anchor point)
            if (phns[x].text in nucleus):
                anchorOns = phns[x].end_time
                anchorCoda = phns[x].start_time
                nInd = x
                segdata.append([wrd, wrdStart, txtgrd, 'S1', 'N', phns[x].text, anchorCoda, anchorOns])
        if nInd == []:
            continue
        if 'o' in stimPOS['S1']:
            onsFirst = stimPOS['S1']['o'][0] #get identity of C1 in onset
            for x in range(0, nInd): #get C1 midpoint
                if phns[x].text == onsFirst:
                    O1Mid = (phns[x].end_time + phns[x].start_time)/2
                    o1 = x
                    segdata.append([wrd, wrdStart, txtgrd, 'S1', 'O1', onsFirst, phns[x].start_time, phns[x].end_time])
            onsLast = stimPOS['S1']['o'][len(stimPOS['S1']['o'])-1] #get identity of final C in onset
            for x in range(0, nInd): #get final C midpoint
                if phns[x].text == onsLast:
                    O2Mid = (phns[x].end_time + phns[x].start_time)/2
                    O2End = phns[x].end_time
            if o1 == []:
                cCenterOns = float("nan")
                rightEdgeMid= float("nan")
                rightEdgeOns = float("nan")
            elif len(stimPOS['S1']['o']) > 1: #calculation of derived stability measurements for complex onsets
                cCenterOns = anchorOns - ((O2Mid - O1Mid)/2)
                rightEdgeMid = anchorOns - O2Mid
                rightEdgeOns = anchorOns - O2End
                segdata.append([wrd, wrdStart, txtgrd, 'S1', 'O2', onsLast, phns[x].start_time, phns[x].end_time])
            else: #calculation of derived stability measurements for simple onsets
                cCenterOns = anchorOns - O1Mid
                rightEdgeMid = anchorOns - O1Mid
                rightEdgeOns = anchorOns - O2End
        else:
            cCenterOns = float("nan")
            rightEdgeMid= float("nan")
            rightEdgeOns = float("nan")
        if 'c' in stimPOS['S1']:
            codaFirst = stimPOS['S1']['c'][0] #get identity of C1 in coda
            for x in range(nInd, len(phns)):
                if phns[x].text == codaFirst:
                    C1Mid = (phns[x].end_time + phns[x].start_time)/2
                    C1Start = phns[x].start_time
                    c1 = x
                    segdata.append([wrd, wrdStart, txtgrd, 'S1', 'C1', codaFirst, phns[x].start_time, phns[x].end_time])
            codaLast = stimPOS['S1']['c'][len(stimPOS['S1']['c'])-1]
            for x in range(nInd, len(phns)):
                if phns[x].text == codaLast:
                    C2Mid = (phns[x].end_time + phns[x].start_time)/2
                    c2 = x
            if c1 == []:
                cCenterCoda = float("nan")
                leftEdgeMid= float("nan")
                leftEdgeOns = float("nan")
            elif len(stimPOS['S1']['c']) > 1: #calculation of coda alignment measurements for complex codas
                if c2 == []:
                    cCenterCoda = float("nan")
                else:
                    cCenterCoda = anchorCoda - ((C2Mid - C1Mid)/2)
                    segdata.append([wrd, wrdStart, txtgrd, 'S1', 'C2', codaLast, phns[x].start_time, phns[x].end_time])
                leftEdgeMid = anchorCoda - C1Mid
                leftEdgeCoda = anchorCoda - C1Start
            else: #calculation of derived alignment measurements for simple codas
                cCenterCoda = anchorCoda - C1Mid
                leftEdgeMid = anchorCoda - C1Mid
                leftEdgeCoda = anchorCoda - C1Start
        else:
            cCenterCoda = float("nan")
            leftEdgeMid = float("nan")
            leftEdgeCoda = float("nan")
        timedata.append([wrd, wrdStart, wrdEnd, txtgrd, 'S1', cCenterOns, rightEdgeMid, rightEdgeOns, cCenterCoda, leftEdgeMid, leftEdgeCoda])
        cCenterOns = float("nan")
        rightEdgeMid = float("nan")
        rightEdgeOns = float("nan")
        cCenterCoda = float("nan")
        leftEdgeMid = float("nan")
        leftEdgeCoda = float("nan")
        if 'S2' in stimPOS:
            o1 = []
            c1 = []
            #c2 = []
            nuc2 = stimPOS['S2']['n'] #get identity of S2 nucleus
            for x in range(nInd+1, len(phns)):
                if (phns[x].text in nuc2):
                    anchorOns2 = phns[x].end_time
                    anchorCoda2 = phns[x].start_time
                    nInd2 = x
                    segdata.append([wrd, wrdStart, txtgrd, 'S2', 'N', phns[x].text, phns[x].start_time, phns[x].end_time])
            if nInd2 == []:
                continue
            if 'o' in stimPOS['S2']:
                onsFirst2 = stimPOS['S2']['o'][0]
                if c2: #set search window based on whether or not preceding syllable had a coda
                    for x in range(c2, nInd2):
                        if phns[x].text == onsFirst2:
                            O1Mid2 = (phns[x].end_time + phns[x].start_time)/2
                            o1 = x
                            segdata.append([wrd, wrdStart, txtgrd, 'S2', 'O1', onsFirst2, phns[x].start_time, phns[x].end_time])
                else:
                    for x in range(nInd+1,nInd2):
                        if phns[x].text == onsFirst2:
                            O1Mid2 = (phns[x].end_time + phns[x].start_time)/2
                            o1 = x
                            segdata.append([wrd, wrdStart, txtgrd, 'S2', 'O1', onsFirst2, phns[x].start_time, phns[x].end_time])
                onsLast2 = stimPOS['S2']['o'][len(stimPOS['S2']['o'])-1]
                if c2:
                    for x in range(c2, nInd2):
                        if phns[x].text == onsLast2:
                            O2Mid2 = (phns[x].end_time + phns[x].start_time)/2
                            O2End2 = phns[x].end_time
                else:
                    for x in range(nInd, nInd2):
                        if phns[x].text == onsLast2:
                            O2Mid2 = (phns[x].end_time + phns[x].start_time)/2
                            O2End2 = phns[x].end_time
                if o1 == []:
                    cCenterOns2 = float("nan")
                    rightEdgeMid2 = float("nan")
                    rightEdgeOns2 = float("nan")
                elif len(stimPOS['S2']['o']) > 1:
                    cCenterOns2 = anchorOns2 - ((O2Mid2 - O1Mid2)/2)
                    rightEdgeMid2 = anchorOns2 - O2Mid2
                    rightEdgeOns2 = anchorOns2 - O2End2
                    segdata.append([wrd, wrdStart, txtgrd, 'S2', 'O2', onsLast2, phns[x].start_time, phns[x].end_time])
                else:
                    cCenterOns2 = anchorOns2 - O1Mid2
                    rightEdgeMid2 = anchorOns2 - O1Mid2
                    rightEdgeOns2 = anchorOns2 - O2End2
            else:
                cCenterOns = float("nan")
                rightEdgeMid= float("nan")
                rightEdgeOns = float("nan")
            if 'c' in stimPOS['S2']:
                codaFirst2 = stimPOS['S2']['c'][0]
                for x in range(nInd2, len(phns)):
                    if phns[x].text == codaFirst2:
                        C1Mid2 = (phns[x].end_time + phns[x].start_time)/2
                        C1Start2 = phns[x].start_time
                        c1 = x
                        segdata.append([wrd, wrdStart, txtgrd, 'S2', 'C1', codaFirst2, phns[x].start_time, phns[x].end_time])
                codaLast2 = stimPOS['S2']['c'][len(stimPOS['S2']['c'])-1]
                for x in range(nInd2, len(phns)):
                    if phns[x].text == codaLast2:
                        C2Mid2 = (phns[x].end_time + phns[x].start_time)/2
                        c2 = x
                if c1 == []:
                    cCenterCoda2 = float("nan")
                    leftEdgeMid2= float("nan")
                    leftEdgeCoda2 = float("nan")
                elif len(stimPOS['S2']['c']) > 1:
                    if c2 == []:
                        cCenterCoda = float("nan")
                    else:
                        cCenterCoda2 = anchorCoda2 - ((C2Mid2 - C1Mid2)/2)
                        segdata.append([wrd, wrdStart, txtgrd, 'S2', 'C2', codaLast2, phns[x].start_time, phns[x].end_time])
                    leftEdgeMid2 = anchorCoda2 - C1Mid2
                    leftEdgeCoda2 = anchorCoda2 - C1Start2
                else:
                    cCenterCoda2 = anchorCoda2 - C1Mid2
                    leftEdgeMid2 = anchorCoda2 - C1Mid2
                    leftEdgeCoda2 = anchorCoda2 - C1Start2
            else:
                cCenterCoda2 = float("nan")
                leftEdgeMid2 = float("nan")
                leftEdgeCoda2 = float("nan")
            timedata.append([wrd, wrdStart, wrdEnd, txtgrd, 'S2', cCenterOns2, rightEdgeMid2, rightEdgeOns2, cCenterCoda2, leftEdgeMid2, leftEdgeCoda2])
            cCenterOns = float("nan")
            rightEdgeMid = float("nan")
            rightEdgeOns = float("nan")
            cCenterCoda = float("nan")
            leftEdgeMid = float("nan")
            leftEdgeCoda = float("nan")
timedf = pd.DataFrame(timedata)
timedf.columns = ['word', 'word_start', 'word_end', 'file', 'syllable', 'ccenter_ons', 
                    'rightedge_mid', 'rightedge_bound', 'ccenter_coda', 
                    'leftedge_mid', 'leftedge_bound']
timedf.to_csv(spkr + "_" + blk + '_derived.csv')

segdf = pd.DataFrame(segdata)
segdf.columns = ['word', 'word_start', 'syllable', 'file', 'position', 'phone', 'phone_start', 'phone_end']
segdf.to_csv(spkr + "_" + blk + "_segments.csv")