#!/usr/bin/env python
# File Name: checkAccuracy.py
# Author: Meiyi (Lexi) He
# Description: a function that used to compare the similarity between strings
# inputs: string A and string B to be compared
# output: percentage (int value) indicates similarity 
# using difflib, SequenceMatcher

from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Test Cases (Examples) below
print similar("apple", "appel")
print similar("apple", "mango")

print similar("I like to eat beets", "why like to meet feet")
print similar("I like to eat beets", "I like to eat meat")
print similar("I like to eat beets", "Like to eat beets")
