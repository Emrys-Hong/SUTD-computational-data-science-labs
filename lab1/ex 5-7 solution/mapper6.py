#!/usr/bin/python

# Format of each line is:
# date\ttime\tstore name\titem description\tcost\tmethod of payment
#
# We need to write our output to standard output, separated by a tab

import sys

for line in sys.stdin:
    data = line.strip().split()
    if len(data) == 10:
        ip, identity, username, datetime, tz, method, page, http_version, status, content_size = data
        print "{0}\t{1}".format(ip, 1)
#we actually don't even need the timestamp for ex.1, just to give a pair here...
