from sys import argv
import os
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

script, filename = argv

print "We're going to write on %r." % filename

target = open(filename, 'w')


# Ask the user to enter the names of files to compare
fname1 = "txt1.txt"
fname2 = "txt2.txt"

f1 = open(fname1)
f2 = open(fname2)

# Print confirmation
print "-----------------------------------"


# Read the first line from the files
f1_line = f1.readline()
f2_line = f2.readline()

# Initialize counter for line number
line_no = 1

# Loop if either file1 or file2 has not reached EOF
while f1_line != '' or f2_line != '':
	target.write( str( similar(f1_line, f2_line) ))

#### TODO: not finished yet

f1_line = f1.readline()
f2_line = f2.readline()

