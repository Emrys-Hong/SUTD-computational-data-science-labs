#!/usr/bin/python

import sys

hitsTotal = 0
oldKey = None

maxHits = 0
popularPage = None

# Loop around the data
# It will be in the format key\tval

for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey, thisHit = data_mapped

    if oldKey and oldKey != thisKey:
	if hitsTotal > maxHits:
	    maxHits = hitsTotal
	    popularPage = oldKey
	
        oldKey = thisKey;
        hitsTotal = 0

    oldKey = thisKey
    hitsTotal += 1

if oldKey != None:
    if hitsTotal > maxHits:
	maxHits = totalHits
	popularPage = oldKey

print popularPage, "\t", maxHits

