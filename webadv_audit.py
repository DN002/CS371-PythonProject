
# Chris A. s1171536, James A. s1032252, Chip J. s#######

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select        # for dropdown menus
from selenium.webdriver.chrome.options import Options   # for 'headless' chrome
import time                                             # implement pauses
from bs4 import BeautifulSoup
import requests

# Write a Python selenium script to parse your info
# The script will normally take one cmd arg:
# python webadv_audit.py s1100841

# If the script has no cmd args, the --help option, or
# an unknown option must display program description & usage

# python3 webadv_audit.py --help

# This Python script retrieves your academic audit and prints a summary. 
# It can optionally save a PDF copy of your entire audit.

# Usage: python3 webadv_audit.py [--option] [student id, e.g., s1100841]	
#    where [--option] can be:
#       --help:	     Display this help information and exit
#       --save-pdf: Save PDF copy of entire audit to the current folder
#                   as audit.pdf
def usageStatement():
   #it must display a program description and program usage statement:
   print("Usage: python3 webadv_audit.py [--option] [student id, e.g., s1100841]")  
   print("where [--option] can be:")
   print("--help:      Display this help information and exit")
   print("--save-pdf: Save PDF copy of entire audit to the current folder")
   print("as audit.pdf")

# Handle args
# arg = sys.argv[1]
# arg = ''
#Will be commented out by hand in, my id is for testing without needing command line
#set to your own id for testing easier
arg = sys.argv[1]

#If the script is run with no commandline arguments,
#CHANGE NUMBER TO ACCURATE REPRESENTATION
if(False):#len(sys.argv) < 1
   usageStatement()#it must display a program description and program usage statement
   exit()
#the --help option,
#CHECK FOR HELP
if(len(sys.argv) > 3):
   if(sys.argv[2] == '--help'):
      usageStatement()#it must display a program description and program usage statement
      exit()


      #If the --save-pdf option was used,
      #CHECK FOR OPTIONS
   elif(sys.argv[2] == '--save-pdf'):
      saveToPDF = True
   #the parsed audit summary must still be displayed,
   #and the PDF of the entire audit must be saved to the current folder as audit.pdf.
   #or an unknown option,
   
    # If the --save-pdf option was used, the 
    # parsed audit summary must still be displayed, and the PDF of 
    # the entire audit must be saved to the current folder as audit.pdf.

   else:
      usageStatement()
      exit()


# use the getpass module to enter the password when trying to login.
# If the password is wrong. display the error message:
# 'Incorrect user ID or password. Exiting.' and exit program
import getpass

# instance of Options class for headless Chrome
options = Options()
# this stops the annoying token error apparently
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Parameter to tell Chrome that it should run with no UI (headless)
# options.headless = False

driver = webdriver.Chrome(options=options)

driver.get('https://webadvisor.monmouth.edu')

# load page
time.sleep(1)

# Clicks the login button
login_select = driver.find_element(By.ID, 'acctLogin')
login_select.click()
time.sleep(1)

# Handle login
# Type username & Enter
username_input = driver.find_element(By.ID, 'userNameInput')
username_input.send_keys(arg)

select_next = driver.find_element(By.ID, 'nextButton')
select_next.click()
time.sleep(1)

# Type password & Enter
password_input = driver.find_element(By.ID, 'passwordInput')
submit_button = driver.find_element(By.ID, 'submitButton')
try:
    p = getpass.getpass(prompt='Enter password for ' + str(arg) + ': ')
    password_input.send_keys(p)
    submit_button.click()
except Exception as error:
    print('ERROR', error)
    print('Incorrect user ID or password. Exiting.')
    exit(-1)
else:
    print('Password entered!')
time.sleep(2)

# select "Students" menu
students_menu = driver.find_element(By.ID, 'mainMenu')
students_menu.click()

# select "Academic Audit / Pgm Eval" link
acadmeic_audit = driver.find_element(By.LINK_TEXT, 'Academic Audit/Pgm Eval')
acadmeic_audit.click()
time.sleep(3)

# select 'Active Program' radio button
radio_button = driver.find_element(By.NAME, 'LIST.VAR1_RADIO')
radio_button.click()
time.sleep(3)

# select 'Submit' button
audit_submit = driver.find_element(By.NAME, 'SUBMIT2')
audit_submit.click()
time.sleep(3)

# parse the following information from your academic audit:
# set up beautiful soup to parse info:
url = driver.current_url
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find("table", id = "StudentTable")

#Your name and student id
studentName = ""
#Program and Catalog
program = ""
#Anticipated Completion Date
antCompleteDate = ""
#Advisor
advisor = ""
#Class Level
classLevel = ""
#Graduation requirements that are "In Progress" (not individual classes)
#
#Graduation requirements that are "Not Started" (not individual classes)
#

#Credits earned at 200+ level (out of 54 required)
higherCredits = ""
#Total credits earned (out of 120 required)
totalCredits = ""

# Successful Retrieval should be like:
# Academic Audit Summary
# ======================
# Name: 		Larlos Cargo (1100841)
# Program:	BA Computer Science (CS.BA)
# Catalog:	C2021
# Anticipated Completion Date:	05/15/23
# ...
# ...
