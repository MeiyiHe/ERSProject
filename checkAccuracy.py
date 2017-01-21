'''Compare the consistency of two strings
   input: two strings to be compared
   output: integer - percentage
'''

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print similar("apple", "appel")
print similar("apple", "mango")