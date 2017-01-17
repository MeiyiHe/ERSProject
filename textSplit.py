


with open("testTxt1.txt") as f:
	lines = f.readlines()
  	for line in lines:
  		words = line.split()
  		for word in words:
  			print (word)