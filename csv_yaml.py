#!/usr/bin/env python3


#############################################
#                                           #
#  Script  to convert csv/xlsx file inputs  #
#  to yaml                                  #
#  Author: DDD Team                         #
#  version 10.0                             #
#                                           #
#############################################

import sys, os
 

# Check python version
if sys.version_info[0] < 3:
	print("Error: Run the script on python3. eg:- \npython3 {}".format(os.path.basename(__file__)))
	sys.exit()
import xlrd, csv, json, yaml, ipaddress, time
import pandas as pd
from collections import  OrderedDict
##Function to convert data into json format(Lists and dictionaries) for effective management. 
##(To be called latter in the script)
def read_csv():
	with open(input_file) as csvfile:
		reader = csv.DictReader(csvfile)
		rows = list(reader)
	json_file = 'json_data.json'
	with open(json_file, "w") as f:
		json.dump(rows, f, sort_keys=True, indent=4, separators=(',', ':'))


##Prompt user for a file input
input_file = input("csv/xlsx file name $ ")


##If input file is a .xlsx file, this variable (xlsx_name) will hold the file name to 
##be renamed to .csv latter in the scrip.  
xlsx_name = input_file.split(".")


##Validate the correct input file formats. 
if not (input_file.endswith('.csv') or input_file.endswith('xlsx')):
	print('csv/xlsx file required')
	sys.exit()


##For a .xlsx file input, read data from the file, output the data to a csv file named after 
## input file name, read the csv data using the read_csv() function and remove the csv file. (Cleanup)
if input_file.endswith('xlsx'):
	try:
		data_xls = pd.read_excel(input_file, 0, index_col=None)
		input_file = xlsx_name[0] + '.csv'
		data_xls.to_csv(input_file, encoding='utf-8', index=False)
		read_csv() # read_csv function call
		os.remove(input_file)

	except FileNotFoundError: #File must be in the same directory as the script. 
		print("No file '{}' in the current path".format(input_file))
		sys.exit()


##For a .csv file input, we call the read_csv() function directly	
else:
	try:
		read_csv() # read_csv function call

	except FileNotFoundError: #File must be in the same directory as the script.
		print("No file '{}' in the current path".format(input_file)) 
		sys.exit()

## All ports to be passed into manipulator() function
ports = {"netbios-ns":137, "137":137, "netbios-dgm":138, '138':138, "netbios-ssn":139, '139':139, "ssh":22, '22':22, "rdp":3389, '3389':3389, "https":443, '443':443, "www":443, "all":-1, "any":-1}

all_data_set = [] # List to hold all data
valid_data_set = [] # List to hold valid data sets.
invalid_data_set = [] # List to hold invalid data sets


def validator():
	##split each value in the Ports collumn(if any) to check for multiple values
	data_set["Port"] = 	data_set["Port"].split()
	
	rd = lambda x: str(x).split('.')[0] # remove decimals lambda 
	rc = lambda x: str(x).split(',')[0] # remove Comma lambda 
	rcol = lambda x: str(x).split(':')[0] # remove Collon lambda
	
	#Handle port data
	def replacedata():
		try:
			data_set["FromPort"], data_set["ToPort"] = int(rd(data_set["Port"][0])), int(rd(data_set["Port"][-1]))
		except ValueError:
			try:
				data_set["FromPort"], data_set["ToPort"] = ports[rc(rcol(data_set["Port"][0]))], ports[rc(rcol(data_set["Port"][-1]))]
			except KeyError:
				data_set["FromPort"], data_set["ToPort"] = rc(rcol(data_set["Port"][0])), rc(rcol(data_set["Port"][-1]))

	# Handle data_sets with port "all", or "any"
	def replace_all_any():
		data_set["FromPort"], data_set["ToPort"], data_set['IpProtocol'] = ports[rc(rcol(data_set["Port"][0]))], ports[data_set["Port"][-1]], ports[rc(rcol(data_set["Port"][0]))]

	##check whether there is a port specified on the spreadsheet provided 
	if data_set["Port"]:
		data_set["Port"] = ([x.lower() for x in data_set["Port"]])

		# single value after spliting port data	
		if len(data_set["Port"]) <= 1:
			data_set["Port"] = data_set["Port"][0].split(',')
			if len(data_set["Port"]) > 1 and not ("all" in data_set["Port"] or "any" in data_set["Port"]):
				replacedata()
			elif "all" in data_set["Port"] or "any" in data_set["Port"]:
				if data_set['Protocol'] == 'ip' or data_set['Protocol'] == "icmp" or data_set['Protocol'] == 'all':
					data_set["FromPort"], data_set["ToPort"], data_set["IpProtocol"] = -1, -1, -1
				else:
					data_set["FromPort"], data_set["ToPort"] = 0, 65535
			
			else:
				data_set["Port"] = data_set["Port"][0].split(':')
				if len(data_set["Port"]) > 1:
					replacedata()
				else:
					replacedata()

		#Multiple values after spliting port data
		else:
			if 'range' in data_set["Port"]:
				data_set["Port"].remove('range')
				replacedata()
			elif "all" in data_set["Port"] or "any" in data_set["Port"]:
				replace_all_any()
			else:
				replacedata()
	

	## If the port section is empty, the script does the required tcp/udp, ip validations
	elif not data_set["Port"] or data_set["Port"] == ' ':
		if (data_set["IpProtocol"] == "tcp" or data_set["IpProtocol"] == "udp"):
			data_set["FromPort"], data_set["ToPort"] = 0, 65535
			
			
		elif data_set["IpProtocol"] == "ip" or  data_set["IpProtocol"] == 'all' or data_set["IpProtocol"] == '' or data_set["IpProtocol"] == ' ':
			data_set["FromPort"], data_set["ToPort"], data_set["IpProtocol"] = -1, -1, -1
		else:
			pass#print(data_set)
	
	del data_set["Protocol"], data_set["Sourcecidr"], data_set["SG Type"], data_set["Port"], data_set["index"]


#Duplicate sets seperated by , and a space 
all_datasets = []
alldata = []
with open('json_data.json', 'r') as y:
	json_data = json.load(y)
	for i, data_set in enumerate(json_data):
		data_set.update({"index":i})
		alldata.append(data_set)
for data_set in alldata:
	if ", " in data_set["Port"]:
		data_set2 = data_set.copy()
		del data_set
		data_set2["Port"] = data_set2["Port"].split(', ')
		for port in data_set2["Port"]:
			data_set3 = data_set2.copy() 
			data_set3["Port"] = port
			
			all_datasets.append(data_set3)
	else:
		all_datasets.append(data_set)

all_datasets = sorted(all_datasets, key=lambda item: item['index']) #Order the data_sets as they are in the input spreadsheet.
with open('data.json', 'w') as outfile: #Create an output json file to hold all_datasets
    json.dump(all_datasets, outfile)

#Read from Json file, perform the manipulation needed to the data.
with open('data.json', 'r') as f:
	json_data = json.load(f)
	for data_set in json_data:
        #Update the script with data to be output on yaml file
		data_set.update({"IpProtocol":data_set["Protocol"], "CidrIp":data_set["Sourcecidr"], "SourceSecurityGroupId":data_set["Sourcecidr"], "FromPort" : '', "ToPort" : ''})
		
		#Check for invalid addressess
		try:
			data_set["CidrIp"] = data_set["CidrIp"].strip()
			data_set["CidrIp"] = str(ipaddress.ip_network(data_set["CidrIp"]))
			#validator()
			del data_set["SourceSecurityGroupId"]
			validator()
			valid_data_set.append(data_set)

		#Empty, "all" or "any"
		except ValueError:
			if (data_set["CidrIp"] == "any" or data_set["CidrIp"] == "all" or data_set["CidrIp"] == ''):
				data_set["CidrIp"] = '0.0.0.0/0'
				del data_set["SourceSecurityGroupId"]
				validator()
				valid_data_set.append(data_set)

			# check for security group IDs
			elif data_set["CidrIp"].startswith("sg-"):
				del data_set["CidrIp"]
				validator()
				valid_data_set.append(data_set)

			# any other is invalid
			else:
				validator()
				invalid_data_set.append(data_set) # Put invaid datasets into the invalid dataset list


## Initialize time, and output files
today = "# Time: " + time.ctime()
Line_break = "#######   End of 50 Rules  #######\n"
output_data = "output.yaml"
invalid_data = "invalid.yaml"

##function to remove quotes on output data.
def strip(input_file):
	FileInput = open(input_file, 'r')
	data = FileInput.read()
	data = data.replace('\'', '')
	FileInput.close()
	FileOutput = open(input_file, "w")
	FileOutput.write(data)
	FileOutput.close()

#Function to remove identical data set.
def discard_identic(input_list):
    add_to_set = set()
    Removed_duplicates = []
    for data_set in input_list:
        tupled_dataset = tuple(data_set.items())
        if tupled_dataset not in add_to_set:
            add_to_set.add(tupled_dataset)
            Removed_duplicates.append(data_set)

    return Removed_duplicates

## Put valid datasets into output.yaml file
if valid_data_set:
	valid_data_set = discard_identic(valid_data_set) #Remove identical datasets
	with open(output_data, 'w') as f: 
		yaml.dump(today, f, default_flow_style=False)
		for i, data_set in enumerate(valid_data_set):
			
			#Insert a line break after every 50 iterations.
			if i % 50 == 0 and not i == 0:
				yaml.dump(Line_break, f, default_flow_style=False)

			#Every set with a SourceSecurityGroupId source
			try:
				# Add a '#' sign to Notes to make it a comment				
				Notes = "# Notes: {}".format(data_set["Notes"])

				# Initialize values to be used by yaml.dump()
				IpProtocol = "- IpProtocol: {}".format(data_set["IpProtocol"])
				FromPort = "  FromPort: {}".format(data_set["FromPort"])
				ToPort = "  ToPort: {}".format(data_set["ToPort"])
				SourceSecurityGroupId = "  SourceSecurityGroupId: {}".format(data_set["SourceSecurityGroupId"])

				# Output each value at a time to maintain defined order.
				yaml.dump(Notes, f, default_flow_style=False)
				yaml.dump(IpProtocol, f, default_flow_style=False)
				yaml.dump(SourceSecurityGroupId, f, default_flow_style=False)
				yaml.dump(FromPort, f, default_flow_style=False)
				yaml.dump(ToPort, f, default_flow_style=False)
				
			#Every set with a cidr block source
			except KeyError:
				CidrIp = "  CidrIp: {}".format(data_set["CidrIp"])
				yaml.dump(Notes, f, default_flow_style=False)
				yaml.dump(IpProtocol, f, default_flow_style=False)
				yaml.dump(CidrIp, f, default_flow_style=False)
				yaml.dump(FromPort, f, default_flow_style=False)
				yaml.dump(ToPort, f, default_flow_style=False)

			#Remove 'Notes' from main output
			del data_set["Notes"]
			
	strip(output_data) ##strip function call 


## Put invalid datasets into invalid.yaml file
if invalid_data_set:
	invalid_data_set = discard_identic(invalid_data_set) #remove identical datasets
	#write into a new invalid.yaml file or append into an existing one	 
	with open(invalid_data, 'a') as file: 
		yaml.dump(today, file, default_flow_style=False)


		for i, inalid_set in enumerate(invalid_data_set):
			
			#Insert a line break after every 50 iterations.
			if i % 50 == 0 and not i == 0:
				yaml.dump(Line_break, file, default_flow_style=False)
		#for inalid_set in invalid_data_set:
			# Add a '#' sign to Notes to make it a comment				
			Notes = "# Notes: {}".format(inalid_set["Notes"])

			# initialize values to be used by yaml.dump()
			IpProtocol = "- IpProtocol: {}".format(inalid_set["IpProtocol"])
			CidrIp = "  CidrIp: {}".format(inalid_set["CidrIp"])
			FromPort = "  FromPort: {}".format(inalid_set["FromPort"])
			ToPort = "  ToPort: {}".format(inalid_set["ToPort"])

			# output each value at a time to maintain defined order.
			yaml.dump(Notes, file, default_flow_style=False)
			yaml.dump(IpProtocol, file, default_flow_style=False)
			yaml.dump(CidrIp, file, default_flow_style=False)
			yaml.dump(FromPort, file, default_flow_style=False)
			yaml.dump(ToPort, file, default_flow_style=False)

			##delete Notes from the main output
			del inalid_set["Notes"]
			
	strip(invalid_data) ##strip function call 


## feedback to user on the output
if valid_data_set and not invalid_data_set:
	print("All addresses are valid\nOutput file:- {}".format(output_data))
elif invalid_data_set and not valid_data_set:
	print("All addresses are invalid\nOutput file:- {}".format(invalid_data))
elif valid_data_set and invalid_data_set:
	print("Some addresses are invalid.\nOutput files:-  {}, {}".format(output_data, invalid_data))
else:
	print("Your input file seems to contain no data")


## Remove json data after code execution
os.remove("json_data.json")
os.remove("data.json")
