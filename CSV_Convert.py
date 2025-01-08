import csv
def read_csv(csvName):
	# opening the CSV file 
	with open(csvName, mode ='r')as file: 
		#list to compare that the field row looks right
		comparator = ['email', 'time', 'message', 'details', 'bundle']
		# reading the CSV file 
		csvFile = csv.reader(file)
		rows = list(csvFile) 
		fields = rows[0]
		
		del rows[0]
		
		print(rows[0],'\n')
		dictRow = list(rows[0])
		print(dictRow[3])
		#detailsSubstring = dict(dictRow[3])
		#for x in detailsSubstring:
		#	print(x, "\n")
		#rowList = list(dictRow.values())
		#print[rowList]
	if fields == comparator:
		print('yes')
	else:
		print('no')
def write_csv(csvName):
    data = [
        {'name': 'Nikhil', 'branch': 'COE', 'year': 2, 'cgpa': 9.0},
        {'name': 'Sanchit', 'branch': 'COE', 'year': 2, 'cgpa': 9.1},
        {'name': 'Aditya', 'branch': 'IT', 'year': 2, 'cgpa': 9.3},
        {'name': 'Sagar', 'branch': 'SE', 'year': 1, 'cgpa': 9.5},
        {'name': 'Prateek', 'branch': 'MCE', 'year': 3, 'cgpa': 7.8},
        {'name': 'Sahil', 'branch': 'EP', 'year': 2, 'cgpa': 9.1}
    ]

    with open('university_records.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'branch', 'year', 'cgpa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
        CSV_Name = 'Sample Events File.csv'
        read_csv(CSV_Name)
if 1 == 1.0:
        main()
