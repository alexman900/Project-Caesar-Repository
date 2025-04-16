# Project-Caesar-Repository
# Purpose: This project is designed to take a .csv file of simulated phishing events and determine whether that interaction came from an ISP leased IP or from an IP that is associated with a known Datacenter. 

#Setup:
  The main python script for this program, CSV_Convert.py, is designed to be run on a single or multiple csv files at a time within either a Kali Linux VM or through any method of running python scripts available to the ISA
The two methods of facilitating this are
  Within a VM:
      Ensure that either bi-directional file drag and drop or a shared folder is configured between your vm and your laptop.
      Download the script and put it in a new folder on the vm with any .csv files you wish to convert
  With any python Runtime environment
      Ensure that the script and any .csv files you wish to convert are in a single folder

API Credentials:
    In order to use this program effectively you should register a free account with ipapi.is to allow you to utilize your own API credential rather than the default API cred associated with developer.
    to do this
    1.go to Ipapi.is
    2.select sign up in the top right of the page
    3. enter the relevent information and create an account
    4. logging in should then take you to the home section of the platform. Your API credential should be listed under its own category
    5. Utilize -c [YOUR API CREDENTIAL HERE] as in argument in any subsequent API calls you make.

      
#Usage:
  With a working python environment available:
  NOTE: You can use any number or combination or arguments and it should work normally
  Convert a Single File:
    -f [filename]
  Convert Multiple Files:
    -fs [Number of Files] [filename] [filename] [filename]
  Assign the api Credentials to use on this call
    -c [API Credential]
  
  The script at most takes about 2 seconds per call so for a project with 500 clicked link and email opened events it would take about 15 minutes to run. (It may run faster or slower depending on your network bandwidth)
      After that all that's needed from the ISA is to determine if the user agent is modern or outdated 
        I would highly advise sorting by the user agent field as most of the user agents will be similar or identical and you should usually have under 100 unique user agents even on a large project

#Anecdote on processing results:

  The script has a few known bugs and a few datacenters that will show up as false even when they are hosted. Genrally the best tool for distinguishing these results is the user agent string
    example:
        you have 20+ user agent strings that match all from the same IP and all the events occurred at right after the email was sent 
        verdict: Clear false positive

  The script will also always show VPS as hosted so sometimes you will have 



  


  


  
      
  
  
