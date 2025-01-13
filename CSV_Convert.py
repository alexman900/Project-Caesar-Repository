import csv
import sys
import requests

def read_csv(csvName,apiCred):
	# opening the CSV file 
	csvName = csvName+".csv"
	print(csvName)
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
		return updateRows(rows,apiCred)
	else:
		print('front fields do not match')
		return None

#takes all rows with the field removed, makes the api calls,
# updates the info, and returns a new array
def updateRows(rows,apiCred):
	newListData =[]
	for i, x in enumerate(rows):
		temprow = list(x)
		if temprow[2] == "Clicked Link" or temprow[2] == "Email Opened":
			IP = str(identifyIP(x[3]))
			#print("Line ", (i+1),": ", IP)
			templist = list(get_posts(IP,apiCred))
			temprow.extend(templist)
			temprow = reformat(temprow)

			newListData.append(temprow)
		else:
			listEmpty = ["","",""]
			temprow.extend(listEmpty)
			temprow = reformat(temprow)
			newListData.append(temprow)

	return newListData

def reformat(templist):
	#fieldnames = ['status/message','ip', 'modified_date/time', 'email','hosted','company_name','details', 'bundle']
	#comparator = ['email', 'modified_date/time', 'status/message, 'details', 'bundle',ip,hosted,companyName]
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
	return templist


#takes a row and extracts and returns the Ip out of it's message column
def identifyIP(row):
	detailsSubstring = str(row)
	detailsList = detailsSubstring.split(":")
	untrimmedIPuseragent = detailsList[4].split(",")
	untrimmedIP=untrimmedIPuseragent[0].split("\"")
	IP=untrimmedIP[1]
	return IP



def get_posts(ipName, apiCred):
	# Define the API endpoint URL
	print(ipName)
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
			
			dictCompany = dict(posts[10])
				
			#split it into values
			listOfCompany = list(dictCompany.values())
			
			#set the first value as the company name
			companyName=listOfCompany[0]
			
			releventData = [ip,hosted,companyName]
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
		fieldnames = ['status/message','ip', 'modified_date/time', 'email','hosted','company_name','details', 'bundle']
		
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
			print("Hithere")
			data.extend(tempdata)
		
	return data
	

# main class to
def main():
	
	
	credentials = 'bdc187a2729c45ed'
	CSV_Names = ['Real_Events_File','Sample Events File']
	newListData = readMultiple_csv(CSV_Names,credentials)
	#for x in newListData:
	#	print(x, '/n')
	write_csv(CSV_Names[0],newListData)

if 1 == 1.0:
	main()
