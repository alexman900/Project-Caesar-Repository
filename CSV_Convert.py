'''
Author: alexman900
File Purpose: This file is designed to take a bulk .csv export of interactions and transform them into a more useful .csv file with additional information on the ip that triggered the interaction


Current information gathered on IPs: currently the script gathers and displays the following additional data on each IP provided:
	Hosted - This boolean indicates whether the IP is owned by a known data center (True) or not (False) using the Ipapi API. Some data center Ips will show up as false due to the api's limitations, these can be double checked against ipinfo as needed as IPinfo tends to be more accurate on this front
	VPN: This boolean indicates whether the IP is a known VPN (True) or not (False) using the Ipapi API. It is fairly inaccurate but useful when dealing with a lot of vpn results.
 	Company Name - This string indicates the company that owns the targeted IP it is almost 100% accurate but may soemtimes show subsidiaries or shell companies in the case of VPNs.
  		Anecdote: Cloudfare and Microsoft are the most common two Hosting companies for VPNs
'''

import csv
import sys
import requests
import os.path
from collections.abc import Iterable


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
		Namecheck=(str(csvName)).split(".")
		return str(Namecheck[0])

	else:
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
	url = 'https://api.ipapi.is?q=' 
	keyString = '&key='
	API_Call=url+ipName+keyString+apiCred
	timeout=10
	print(API_Call)

	try:
		# Make a GET request to the API endpoint using requests.get()
		response = requests.get(API_Call, timeout)
		# Check if the request was successful (status code 200)
		if response.status_code == 200:
			#create a dictionary of the json response
			json = response.json()
			#break that dictionary up into its corresponding values
			posts = list(json.values())
			#value 1 is the ip searched
			ip = posts[0]
			#value 6 is a boolen of hosted or not
			hosted = posts[6]
			#value 9 is the value of whether the call is a vpn or not
			vpn = posts[9]
			print(posts[9])

			#convert the company string to a dictionary,
			if isinstance(posts[10], Iterable):
				dictCompany = dict(posts[10])
				listOfCompany = list(dictCompany.values())
			else:
				if isinstance(posts[11], Iterable):
					dictCompany = dict(posts[11])
					listOfCompany = list(dictCompany.values())
				else:
					if isinstance(posts[12], Iterable):
						dictCompany = dict(posts[12])
						listOfCompany = list(dictCompany.values())
					else:
						print("Error 1 unhandled API case for: ", ip)
						listOfCompany = ["Unknown"]
			#set the first value as the company name
			companyName=listOfCompany[0]
			
			releventData = [ip,hosted,companyName,userAgent]
			return releventData
		elif response.status_code == 403
			print('Error the api call:', API_Call, '\n returned error code : ') response.status_code, '\n this indicates that the IPAPI server recognizes this call but refused to return results.)
			print('This is likely means that the API key you are using has exceeded its 1000 call per day capacity.\nIf you are using the default credential, please register a free api key at https://ipapi.is/app/signup to use with the -c command or hardcode the default to be your api key')
			print('if you are not using the default key and believe you have not exceeded the 1000 call limit (eg your csv files did not have a total count of 1000 lines with a user agent field), this may be caused by operating on an ip which you did not register the account on try disconnecting from a vpn or connecting to ours')
			return None
		elif response.status_code == 503
			print('Error the api call:', API_Call, ' returned an error response code: ') response.status_code, '\n this indicates that the IPAPI.is servers are down.\n You can confirm this at https://ipapi.is/app/request-builder by checking if their test api "Try It" option is working.)
			return None
		else 
			print('Error the api call:', API_Call, ' returned an error response code: ') response.status_code, 'Something has gone wildly wrong. Please contact alexman900 for assistance')
			return None
	except requests.exceptions.RequestException as e:
		print('Error: ', e,'\nTry catch block failed for getposts function. Please contact alexman900 for assistance:')
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




#command line parser functions
def parseCommandLine(argv):
	"""
	this is a test does this show in hover

 	Args:
  		argv (array): this is the first arg
    	Returns:
     		array: the array result of command line args
 	"""
	templist = list(argv)
	noFileList = False;
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
				print((checkCSVName(templist[1]) + ".csv"), " exists")
				del templist[0]
				del templist[0]
			else:
				print((checkCSVName(templist[1]) + ".csv"), " does not exist")
				del templist[0]
				del templist[0]

		elif (str(templist[0]) == "-fs"):
			if int(templist[1]) >=1:
				FileCount = (int(templist[1]))
				i = 0;
				while i < FileCount:
					if os.path.isfile(checkCSVName(templist[i+2]) + ".csv"):
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
				print("Error 2nd arg in -fs was not a number greater than 0")				
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
		
	if len(filelist) < 1:
		fileListExists = 1
		returnList.append(fileListExists)
	
	
	elif APICredential == "empty":
		fileListExists = 2
		returnList.append(fileListExists)
		returnList.append(filelist)
		

	else:
		fileListExists = 3
		returnList.append(fileListExists)
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

# main class to run the actual code
def main():
	
	n = len(sys.argv)
	args = list(sys.argv)
	newListData = []
	#If you wante to hardcode the API Credentials to your own change the line below to your API credentials
	credentials = 'bdc187a2729c45ed'
	if len(args) >= 2:
		returnlist = parseCommandLine(args)
		if returnlist[0] == 3:
			CSV_Names= returnlist[1]
			print("FileList: \n",returnlist[1])
			credentials = returnlist[2]
			print("NewAPICredentials: ",returnlist[2])
			newListData = readMultiple_csv(CSV_Names,credentials)
			write_csv(CSV_Names[0],newListData)
		
		elif returnlist[0] == 2:
			CSV_Names= returnlist[1]
			print("FileList: \n",returnlist[1])
			newListData = readMultiple_csv(CSV_Names,credentials)
			write_csv(CSV_Names[0],newListData)
	
	
	else:
		printHelpMethod()
	

if 1 == 1.0:
	main()
