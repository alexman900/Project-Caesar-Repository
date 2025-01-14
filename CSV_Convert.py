import csv
import sys
import requests
import os.path


def read_csv(csvName,apiCred):
	# opening the CSV file 
	csvNamecheck =csvName
	csvName = csvName+".csv"
	
	with open(csvName, mode ='r')as file: 
		#list to compare that the field row looks right
		comparator = ['email', 'time', 'message', 'details', 'bundle']
		# reading the CSV file 
		csvFile = csv.reader(file)
		rows = list(csvFile) 

		#update the fields row to make sure this file at least seems valid
		fields = rows[0]
		#remove the fields row
		del rows[0]

	if fields == comparator:
		data= updateRows(rows,apiCred)
		if data:
			print(csvName, " read successfully")
		else:
			print(csvName, " could not be read")
			
		return data
	else:
		print('front fields do not match')
		return None
		
def checkCSVName(csvName):
	if "." in (str(csvName)):
		Namecheck=(str(cvsName)).split(".")
		return str(Namecheck[0])
	else
		return str(csvName)
	

	

#takes all rows with the field removed, makes the api calls,
# updates the info, and returns a new array
def updateRows(rows,apiCred):
	newListData =[]
	for i, x in enumerate(rows):
		temprow = list(x)
		if temprow[2] == "Clicked Link" or temprow[2] == "Email Opened":
			IP = str(identifyIP(x[3]))
			userAgent = str(identifyUserAgent(x[3]))
			#print("Line ", (i+1),": ", IP, userAgent)
			templist = list(get_posts(IP,apiCred, userAgent))
			temprow.extend(templist)
			temprow = reformat(temprow)

			newListData.append(temprow)
		else:
			listEmpty = ["","","",""]
			temprow.extend(listEmpty)
			temprow = reformat(temprow)
			newListData.append(temprow)

	return newListData

def reformat(templist):
	#fieldnames = ['status/message','ip', 'modified_date/time', 'email','hosted','company_name',' user agent', 'details', 'bundle']
	#comparator = ['email', 'modified_date/time', 'status/message, 'details', 'bundle',ip,hosted,companyName, user agent]
	#swap email and status/message	
	templist[0], templist[2] = templist[2], templist[0];
	#swap modified_date/time and ip	
	templist[1], templist[5] = templist[5], templist[1];
	#swap email and modified_date/time
	templist[2], templist[5] = templist[5], templist[2];
	#swap email and 
	templist[3], templist[5] = templist[5], templist[3];
	#swap status/message and modified_date/time
	templist[4], templist[6] = templist[6], templist[4];
	#['status/message','ip', 'modified_date/time', 'email','hosted',details, bundle, company
	templist[5], templist[7] = templist[7], templist[5];
	templist[6], templist[7] = templist[6], templist[7];
	templist[6], templist[7] = templist[6], templist[7];
	templist[6], templist[8] = templist[8], templist[6];
	templist[7], templist[8] = templist[8], templist[7];
	return templist


#takes a row and extracts and returns the Ip out of it's message column
def identifyIP(row):
	detailsSubstring = str(row)
	detailsList = detailsSubstring.split(":")
	untrimmedIPuseragent = detailsList[4].split(",")
	untrimmedIP=untrimmedIPuseragent[0].split("\"")
	IP=untrimmedIP[1]
	return IP

def identifyUserAgent(row):
	detailsSubstring = str(row)
	detailsList = detailsSubstring.split(":")
	untrimmedUseragent = detailsList[5].split("\"")
	Agent=untrimmedUseragent[1]
	return Agent


def get_posts(ipName, apiCred, userAgent):
	# Define the API endpoint URL
	#print(ipName)
	url = 'https://api.ipapi.is/?q=' 
	keyString = '&key='
	API_Call=url+ipName+keyString+apiCred

	try:
		# Make a GET request to the API endpoint using requests.get()
		response = requests.get(API_Call)
		# Check if the request was successful (status code 200)
		if response.status_code == 200:
			#create a dictionary of the json response
			json = response.json()
			#break that dictionary up into its corresponding values
			posts = list(json.values())
			#value 1 is the ip searched
			ip = posts[0]
			#value 6 is a boolen of hosted or not
			hosted = posts[5]

			#convert the company string to a dictionary,
			if()
			dictCompany = dict(posts[10])
			print ("I'm MR Helper PRint LOOK AT ME: ", dictCompany)
			#split it into values
			listOfCompany = list(dictCompany.values())
			
			#set the first value as the company name
			companyName=listOfCompany[0]
			
			releventData = [ip,hosted,companyName,userAgent]
			return releventData
		else:
			print('Error:', response.status_code)
			return None
	except requests.exceptions.RequestException as e:
		print('Error:', e)
		return None


#take a .csv passed as a filename and a data element and write  it to a file named after the csv file
def write_csv(csvName, data):

	newCSVName = csvName + "_with_Hosting_Marked.csv"
	for x in data: 
		fieldnames = ['status/message','ip', 'modified_date/time', 'email','hosted','company_name','user_agent','bundles', 'details']
		
	with open(newCSVName, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fieldnames)
		writer.writerows(data)

#recursive class to call read_csv on mutiple csv files and append the results into one data List for writing
def readMultiple_csv(csvNames,credentials):
	data = []
	for x in csvNames:
		tempdata = read_csv(x,credentials)
		if tempdata:
			data.extend(tempdata)
		
	return data





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
			if os.path.isfile((checkCSVName(templist[1]) + ".csv")):
				filelist.append(checkCSVName(templist[1]))
				print(checkCSVName(templist[1]) + ".csv"), " exists")
				del templist[0]
				del templist[0]
			else:
				print(checkCSVName(templist[1]) + ".csv"), " does not exist")
				del templist[0]
				del templist[0]

		elif (str(templist[0]) == "-fs"):
			if int(templist[1]) >=1:
				FileCount = (int(templist[1]))
				i = 0;
				while i < FileCount:
					if os.path.isfile(checkCSVName(templist[i+2]) + ".csv")):
						print((checkCSVName(templist[i+2]) + ".csv"), " exists")
						filelist.append(checkCSVName(templist[i+2]))
						i = i+1
					else:
						print((checkCSVName(templist[i+2]) + ".csv"), " does not exist")
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

# main class to
def main():
	
	n = len(sys.argv)
	args = list(sys.argv)
	newListData = []
	credentials = 'bdc187a2729c45ed'
	if len(args) > 1:
		returnlist = parseCommandLine(args)
		if len(returnlist) > 1:
			CSV_Names= returnlist[0]
			
			print("FileList: \n",returnlist[0])
			credentials = returnlist[1]
			print("NewAPICredentials: ",returnlist[1])
		else:
			CSV_Names= returnlist[0]
			print("FileList: \n",returnlist[0])

		newListData = readMultiple_csv(CSV_Names,credentials)
		write_csv(CSV_Names[0],newListData)
	else:
		printHelpMethod()
	

if 1 == 1.0:
	main()
