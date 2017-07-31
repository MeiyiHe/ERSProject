import argparse
from genLib_m import genLib_m
from genLib_p import genLib_p
import sys
import os.path
import subprocess

#get arguments from the command line
parser = argparse.ArgumentParser(
	description="This program updates a user library by inputting a script and its corresponding audio.",
	epilog="Thanks for using our program.")
parser.add_argument('-u', nargs='?', default='abk', type=str,										
					help="username, default is 'abk'")                  
parser.add_argument('-f', nargs='?', type=str, required=True, 
					help="input_file(relative path) - the file used to generate the user library")
parser.add_argument('-align', choices=['m','p','b'], default='b', 
					help="pick the aligner to use [m-Montreal, p-Prosody, b-both(default)]")

args = parser.parse_args()
username = args.u
input_file = args.f
aligner = args.align

#check if the user library exists
if not os.path.isdir(username):
	print("The user library - {} doesn't exist!\n".format(username))
	var = raw_input("If you want to create a new user library, please enter '1'.\n" \
					"If you want to exit, please enter'2'.\n\n"\
					"Please enter here:")
	print('')
	while(True):
		if var == '1':
			var = raw_input("Please enter the username:")
			print('')
			while (True):
				if var:
					yorn = raw_input("Is '{}' the username you want to input?[y/n]".format(var))
					print('')
					if yorn == 'y' or yorn == 'Y':
						#create the folder
						os.makedirs(var)
						print("Congratulations! The user library - {} is created!".format(var))
						break
					elif yorn == 'n' or yorn == 'N':
						var = raw_input("Please reenter the username:")
						print('')
					else:
						print("Sorry, your input is not valid.\n")
				else:
					var = raw_input("Please enter the username:\n")
					print('')
			break
		elif var == '2':
			print("Thanks for using our program!")
			print("System is exiting ... ... ")
			sys.exit(-1)
		else:
			var = raw_input("Sorry, your input is invalid. Please input '1' or '2' only.\n" \
					"If you want to create a new user library, please enter '1'.\n" \
					"If you want to exit, please enter'2'.\n")

###########################################
# user folder system will be handled later #
###########################################

if aligner == 'b':
	print("Generating the user library from Montreal ... ... ")
	genLib_m(username, input_file)
	print("Generating the user library from Prosody ... ... ")
	genLib_p(username, input_file)
elif aligner == 'm':
	print("Generating the user library from Montreal ... ... ")
	genLib_m(username, input_file)
else:
	print("Generating the user library from Prosody ... ... ")
	genLib_p(username, input_file)



