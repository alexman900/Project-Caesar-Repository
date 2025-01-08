import requests



def get_posts(ipName, apiCred):
	# Define the API endpoint URL
	url = 'https://api.ipapi.is/' 
	keyString = '&key='
	API_Call=url+ipName+keyString+apiCred

	try:
		# Make a GET request to the API endpoint using requests.get()
		response = requests.get(url)
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



def main():
	credentials = 'bdc187a2729c45ed'
	ipname = '174.192.5.14'
	releventData = get_posts(ipname,credentials)
	print(releventData[0], '\n')
	print(releventData[1], '\n')
	print(releventData[2], '\n')

if 1 == 1.0:
	main()