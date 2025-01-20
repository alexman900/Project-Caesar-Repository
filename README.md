# Project-Caesar-Repository
# Purpose: This project is designed to take a .csv file of simulated phishing events and determine whether that interaction came from an ISP leased IP or from an IP that is associated with a known Datacenter. 

#Setup:
  The main python script for this program, CSV_Convert.py, is designed to be run on a single or multiple csv files at a time within either a Kali Linux VM or through any method of running python script available to the ISA
The two methods of facilitating this are
  Within a VM:
      Ensure that either bi-directional file drag and drop or a shared folder is configured between your vm and your laptop.
      Download the script and put it in a new folder on the vm with any .csv files you wish to convert
  With any python Runtime environment
      Ensure that the script and any .csv files you wish to convert are in a single folder
      
#Usage:
  With a working python environment available:
      Single .csv File: 
            Run the following command
            python3 CSV_Convert.py -f [filename]
            NOTE: Do not add .csv to the end of the name just give the exact name it has
      Mutiple .csv Files:
            Run the following command
            python3 CSV_Convert.py -fs [filename1], [filename2],...
            NOTE: Do not add .csv to the end of the name just give the exact name it has
      The script takes about 2 seconds per call so for a project with 500 clicked link and email opened events it would take about 15 minutes to run.
      After that all that's needed from the ISA is to determine if the user agent is modern or outdated 
        I would advise sorting by the user agent string field I

  
      
  
  
