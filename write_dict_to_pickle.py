#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:37:33 2022

@author: sarahharper
"""

import pickle
import os

os.chdir('/Users/sarahharper/Dropbox/ChangLab/Syllable_Boundary/')

#define dictionary
wrds = {'day': {'S1' : {'o': 'D', 'n': 'EY1'}},
        'ay': {'S1' : {'n': 'EY1'}},
        'aid':  {'S1' : {'n': 'EY1', 'c' : 'D'}},
        'say': {'S1' : {'o': 'S', 'n' : 'EY1'}},
        'ace': {'S1' : {'n':'EY1', 'c' : 'S'}},
        'may': {'S1' : {'o' : 'M', 'n' : 'EY1'}}, 
        'aim': {'S1': {'n' : 'EY1', 'c' : 'M'}},
        'a': {'S1' : {'n': ['AH0', 'EY1']}},
        'pop': {'S1' : {'o': 'P', 'n': 'AA1', 'c' : 'P'}},
        'papa': {'S1' : {'o' : 'P', 'n' : 'AA1'}, 'S2' : {'o' : 'P', 'n': 'AH0'}},
        'mom' : {'S1' : {'o': 'M', 'n' : 'AA1', 'c': 'M'}},
        'mama' :{'S1' : {'o': 'M', 'n': 'AA1'}, 'S2' : {'o' : 'M', 'n' : 'AH0'}},
        'grade' : {'S1' : {'o': ['G', 'R'], 'n': 'EY1', 'c' : 'D'}},
        'gray' : {'S1' : {'o' : ['G', 'R'], 'n': 'EY1'}},
        'grey' : {'S1' : {'o' : ['G', 'R'], 'n': 'EY1'}},
        'lay' : {'S1' : {'o' : 'L', 'n': 'EY1'}},
        'span' : {'S1' : {'o' : ['S', 'P'], 'n': 'AE1', 'c': 'N'}},
        'lace' : {'S1' : {'o' : 'L', 'n' : 'EY1', 'c':'S'}},
        'pan' : {'S1' : {'o' : 'P', 'n' : 'AE1', 'c': 'N'}},
        'freely' : {'S1': {'o' : ['F', 'R'], 'n': 'IY1'}, 'S2' : {'o': 'L', 'n': 'IY0'}},
        'free' : {'S1': {'o' : ['F','R'], 'n': 'IY1'}},
        'lee' : {'S1': {'o' : 'L', 'n' : 'IY1'}},
        'sack' : {'S1' : {'o' : 'S', 'n': 'AE1', 'c' : 'K'}},
        'axe' : {'S1': {'n' : 'AE1', 'c' : ['K', 'S']}},
        'trip' : {'S1' : {'o' : ['T', 'R'], 'n': 'IH1', 'c': 'P'}},
        'ripped' : {'S1' : {'o' : 'R', 'n' : 'IH1', 'c': ['P', 'T']}},
        'tray' : {'S1' : {'o' : ['T', 'R'], 'n': 'EY1'}},
        'rate' : {'S1' : {'o' : 'R', 'n': 'EY1', 'c': 'T'}},
        'copes' : {'S1' : {'o' : 'K', 'n' : 'OW1', 'c': ['P', 'S']}},
        'cope' : {'S1' : {'o' : 'K', 'n' : 'OW1', 'c': ['P']}},
        'scope' :{'S1' : {'o' : ['S', 'K'], 'n': 'OW1', 'c' : 'P' }},
        'tulips' : {'S1' : {'o' : 'T', 'n' : 'UW1'}, 'S2' : {'o' : 'L', 'n': 'AH0', 'c' : ['P', 'S']}},
        'tulip' : {'S1' : {'o' : 'T', 'n' : 'UW1'}, 'S2' : {'o' : 'L', 'n': 'AH0', 'c' : 'P'}},
        'two' : {'S1' : {'o': 'T', 'n' : 'UW1'}},
        'lips' : {'S1' : {'o' : 'L', 'n' : 'IH1', 'c': ['P', 'S']}},
        'inform' : {'S1' : {'n': 'IH0', 'c' : 'N'}, 'S2' : {'o': 'F', 'n' : 'AO1', 'c': ['R', 'M']}},
        'foreman' : {'S1' : {'o' : 'F', 'n' : 'AO1', 'c' : 'R'}, 'S2' : {'o' : 'M', 'n': 'AH0', 'c' : 'N'}},
        'tables' : {'S1' : {'o' : 'T', 'n' : 'EY1'}, 'S2' : {'o' : 'B', 'n' : 'AH0', 'c' : ['L', 'Z']}},
        'stable' : {'S1' : {'o' : ['S', 'T'] , 'n' : 'EY1'}, 'S2' : {'o' : 'B', 'n' : 'AH0', 'c' : 'L'}},
        'stables' : {'S1' : {'o' : ['S', 'T'] , 'n' : 'EY1'}, 'S2' : {'o' : 'B', 'n' : 'AH0', 'c' : ['L', 'Z']}},
        'plum' : {'S1' : {'o' : ['P', 'L'], 'n' : 'AH1', 'c' : 'M'}},
        'pie' : {'S1' : {'o' : 'P', 'n' : 'AY1'}},
        'bie' : {'S1' : {'o' : 'B', 'n' : 'AY1'}},
        'plump' : {'S1' : {'o' : ['P', 'L'], 'n' : 'AH1', 'c' : ['M', 'P']}},
        'ply' : {'S1' : {'o' : ['P', 'L'], 'n' : 'AY1'}},
        'eye' : {'S1' : {'n' : 'AY1'}},
        're' : {'S1' : {'o' : ['R'], 'n' : 'EY1'}},
        's' : {'S1' : {'n' : ['S']}},
        'pum' : {'S1' : {'o': ['P'], 'n': ['UH1'], 'c': ['M']}},
        'lie': {'S1': {'o': ['L'], 'n': ['AY1']}},
        'error': {'S1': {'n': ['NA']}},
        'pump': {'S1': {'o' : 'P', 'n': 'UH1', 'c':['M', 'P']}}}

#create a binary pickle file
f = open('syll_bound_pos.pkl', 'wb')

#write dict to pickle
pickle.dump(wrds, f)

f.close()
