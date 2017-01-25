from collections import Counter
# this function can be used to count how many words in a file

c = Counter()
with open('txtscripts1.txt', 'rb') as f:
    for ln in f:
        c.update(ln.split())

total1 = sum(c.values())
print total1
#specific = c['']

#####################################################################
c = Counter()
with open('srScripts1.txt', 'rb') as f:
    for ln in f:
        c.update(ln.split())

total2 = sum(c.values())
print total2


