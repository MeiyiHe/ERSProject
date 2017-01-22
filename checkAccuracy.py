'''Compare the consistency of two strings
   input: two strings to be compared
   output: integer - percentage
'''

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print similar("apple", "appel")
print similar("apple", "mango")

print similar("I like to eat beets", "why like to meet feet")
print similar("I like to eat beets", "I like to eat meat")
print similar("I like to eat beets", "Like to eat beets")