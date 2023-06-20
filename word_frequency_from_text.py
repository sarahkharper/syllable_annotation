#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 01:24:34 2022

@author: sarahharper
"""

from collections import Counter
import os

os.chdir("/Users/sarahharper/Dropbox/My Mac (Sarah’s MacBook Pro)/Downloads")
fname = "IEEE_Gloss.txt"
def word_count(fname):
        with open(fname) as f:
                return Counter(f.read().split())

print("Number of words in the file :",word_count("IEEE_Gloss.txt"))

was
with
on
into
that
when
than
old
strong
up
they
makes
used
yong
before
thin
she
red
round 
fine
small
sharp
kept
way 
bright
this
good
box
large
left
two
make 
each
brown
most
new
made
best
last
down
blue
clear
back
tall
third
wide
dull
dont
these
took
green
white
now 
they
like 
gold
both
takes
Take
work
boy
tea 
get 
lack
came
grass
over 
show
their
first
ran 
set 
this
water
big
more
door
deep
along