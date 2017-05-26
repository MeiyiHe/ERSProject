

def rewritten():
	f1 = open('a.txt', 'r')
	f2 = open('b.txt', 'w')
	for line in f1:
	    f2.write(line.replace('?', '2'))
	f1.close()
	f2.close()
	return f2