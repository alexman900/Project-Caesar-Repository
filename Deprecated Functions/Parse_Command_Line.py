# Python program to demonstrate
# command line arguments
# .isfile(path)

import os.path
import sys


def parseCommandLine(argv):
	templist = list(argv)
	print(templist)
	del templist[0]
	APICredential = "empty"
	returnList = []
	filelist = [];
	if len(templist) == 1:
		if (str(templist[0]) == "-h"):
			printHelpMethod()			
	
			del templist[0]
		else:
			print("Error ", templist[0], " is not a valid argument /n Please use -h to get the list of valid arguments")
			templist.clear()

	while len(templist) >= 2:
		if (str(templist[0]) == "-f"):
			if os.path.isfile((str(templist[1]) + ".csv")):
				filelist.append(str(templist[1]))
				print((str(templist[1]) + ".csv"), " exists")
				del templist[0]
				del templist[0]
			else:
				print((str(templist[1]) + ".csv"), " does not exist")
				del templist[0]
				del templist[0]

		elif (str(templist[0]) == "-fs"):
			if int(templist[1]) >=1:
				FileCount = (int(templist[1]))
				i = 0;
				while i < FileCount:
					if os.path.isfile((str(templist[i+2]) + ".csv")):
						print((str(templist[i+2]) + ".csv"), " exists")
						filelist.append(str(templist[i+2]))
						i = i+1
					else:
						print((str(templist[i+2]) + ".csv"), " does not exist")
						i = i+1
				i = 0;
				while i < FileCount:
					del templist[2]
					i = i+1
				del templist[0]
				del templist[0]
			else:
				print("error 2nd arg in -fs was not a number greater than 0")				
				templist.clear()
							

		elif (str(templist[0]) == "-h"):
			printHelpMethod()
			del templist[0]

		elif (str(templist[0]) == "-c"):
			#do something
			print("APICRED Should be: ", str(templist[1]))
			APICredential = str(templist[1])
			del templist[0]
			del templist[0]
		else:
			print("Error ", templist[0], " is not a valid argument /n Please use -h to get the list of valid arguments")
			templist.clear()
	if APICredential == "empty":
		returnList.append(filelist)

	else:
		returnList.append(filelist)
		returnList.append(APICredential)	
		
	return returnList
	
def printHelpMethod():
	print("Usage: \n")
	print("\t python3 CSV_Convert.py [OPTIONS]")
	print("\n")
	print("Argument Options: \n")
	print("\t -f [filename]\t\t Convert a Single File")
	print("\t -fs [Number of Files] [filename] [filename] [filename] ...\t\t Convert a Multiple File Please leave out .csv")
	print("\t -c [API Credential]\t\t Define an API Credential besides the default")
	print("\t -h help method")

def main():
	# total arguments
	n = len(sys.argv)
	args = list(sys.argv)
	print("Total arguments passed:", n)
	
	# Arguments passed
	print("\nName of Python script:", sys.argv[0])
	
	for i, x in enumerate(args):
		print("Argument ", i+1, ": ", x)
	APICredential = ""
	if len(args) > 1:
		returnlist = parseCommandLine(args)
		if len(returnlist) > 1:
			print("FileList: \n",returnlist[0])
			print("NewAPICredentials: ",returnlist[1])
		else:
			print("FileList: \n",returnlist[0])
			
	else:
		printHelpMethod()


if 1 == 1.0:
	main()
