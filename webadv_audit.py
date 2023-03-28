
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

# Chris A. s#######, James A. s1032252, Chip J. s#######

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select        # for dropdown menus
from selenium.webdriver.chrome.options import Options   # for 'headless' chrome
import time                                             # implement pauses

# Handle args
# arg = sys.argv[1]
arg = 's1171536'

# use the getpass module to enter the password when trying to login.
# If the password is wrong. display the error message:
# 'Incorrect user ID or password. Exiting.' and exit program
import getpass

# instance of Options class for headless Chrome
options = Options()

# Parameter to tell Chrome that it should run with no UI (headless)
# options.headless = True

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
try:
    p = getpass.getpass(prompt='Password?')
except Exception as error:
    print('ERROR', error)
    print('Incorrect user ID or password. Exiting.')
    exit(-1)
else:
    print('Password entered!')

time.sleep(2)

# Submit if all good, exit with error if bad

# select "Students" menu

# select "Academic Audit / Pgm Eval" link

# select 'Active Program' radio button

# select 'Submit' button

# Successful Retrieval should be like:
# Academic Audit Summary
# ======================
# Name: 		Larlos Cargo (1100841)
# Program:	BA Computer Science (CS.BA)
# Catalog:	C2021
# Anticipated Completion Date:	05/15/23
# ...
# ...

# If the --save-pdf option was used, the 
# parsed audit summary must still be displayed, and the PDF of 
# the entire audit must be saved to the current folder as audit.pdf.