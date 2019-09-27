INSTRUCTIONS:
1. Python script runs on  python3+.
2. Configure the required modules as highlited on the prerequisites.
3. The script takes as input files with a .xlsx extension.
 

PREREQUISITES:
​ Linux (Ubuntu):-
	Terminal
		1. Install python3-pip
			$ sudo apt-get install python3-pip
		2. Install pandas
			$ pip3 install pandas
		3. install xlrd 
			$ pip3 install xlrd 
		4. install pyyaml
			$ pip3 install pyyaml

 ​Windows:-

	CMD
		1. Install python3-pip
			(visit link to install) https://bootstrap.pypa.io/3.3/get-pip.py
		2. Install pandas
			$ pip3 install pandas
		3. install xlrd 
			$ pip3 install xlrd 
		4. install pyyaml
			$ pip3 install pyyaml
		



TESTING:- (Ubuntu)
	1. Unpack the package.
		$ unzip Task_8.zip
	2. List 'Task_8' directory contents
		$ls -l

		README.txt
		Sample_Input.xlsx
		yaml_dumpv6.py

	3. run the script

			./yaml_dump.py
		$ csv/xlsx file name $ 

	
			a. For non csv/xlsx files:-

		csv/xlsx file name $ sample.txt
		$ csv/xlsx file required

			b. For csv/xlsx files not within the directory:- 

		csv/xlsx file name $ sample.xlsx
		$ No file 'sample.xlsx' in the current path

			3. For a functional operation, the output is stored on the working directory as:

		csv/xlsx file name $ Sample_Input.xlsx
		output file:- output.yaml


			4. $ ls -l

		output.yaml
		invalid.yaml
		README.txt
		Sample_Input.xlsx
		yaml_dump.py



------------------------------------------------------------------------------------------------------------------	
		File Details
------------------------------------------------------------------------------------------------------------------
		FILE					DETAILS
		output.yaml 			File containing yaml output
		invalid.yaml            File containing invalid output
		README.txt				Instructions & Brief Explanation text file.
		Sample_Input.xlsx		Input file containing data to be manipulated.
		yaml_dumpv2.py			Script perfoming the manupulation.
------------------------------------------------------------------------------------------------------------------