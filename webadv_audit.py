# Chris A. s1171536, James A. s1032252, Chip J. s1248459
# CS 371

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options   # for 'headless' chrome
import time                                             # implement pauses
import requests, bs4
import os
import json
from pyhtml2pdf import converter

# use the getpass module to enter the password when trying to login.
# If the password is wrong. display the error message:
# 'Incorrect user ID or password. Exiting.' and exit program
import getpass

# instance of Options class for headless Chrome
options = Options()
# this stops the annoying token error apparently
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--enable-javascript")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--kiosk-printing')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('https://webadvisor.monmouth.edu')
savePDF = False

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

# function that saves the input html to a pdf file
def saveToPDF(pdf_html):
   with open('page.html', 'w') as f:
      f.write(pdf_html)
   if os.path.exists('audit.pdf'):
      os.remove('audit.pdf')
   path = os.path.abspath('page.html')
   driver.maximize_window()
   time.sleep(5)
   converter.convert(f'file:///{path}', 'audit.pdf')
   os.remove('page.html')

# function to print usage statement
def usageStatement():
   # it must display a program description and program usage statement:
   print("Usage: python3 webadv_audit.py [--option] [student id, e.g., s1100841]")  
   print("where [--option] can be:")
   print("--help:      Display this help information and exit")
   print("--save-pdf: Save PDF copy of entire audit to the current folder")
   print("as audit.pdf")

#If the script is run with no commandline arguments,
#CHANGE NUMBER TO ACCURATE REPRESENTATION
if(len(sys.argv) < 1):
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
      savePDF = True
      # If the --save-pdf option was used, the 
      # parsed audit summary must still be displayed, and the PDF of 
      # the entire audit must be saved to the current folder as audit.pdf.


   else:
      usageStatement()
      exit()

try:
   arg = sys.argv[1]
except:
   usageStatement()
   exit()

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

# select "Students" menu
students_menu = driver.find_element(By.ID, 'mainMenu')
students_menu.click()
time.sleep(1)

# select "Academic Audit / Pgm Eval" link
acadmeic_audit = driver.find_element(By.LINK_TEXT, 'Academic Audit/Pgm Eval')
acadmeic_audit.click()
time.sleep(1)

# select 'Active Program' radio button
radio_button = driver.find_element(By.NAME, 'LIST.VAR1_RADIO')
radio_button.click()
time.sleep(1)

# select 'Submit' button
audit_submit = driver.find_element(By.NAME, 'SUBMIT2')
audit_submit.click()
time.sleep(1)

# finding parent elements for each audit element
audit_table = driver.find_element(By.XPATH, "//table[@id='StudentTable']")
studentName = audit_table.find_element(By.CLASS_NAME, 'PersonName')
program_td = driver.find_element(By.XPATH, "// td[contains(text(),\
'Program: ')]")
program_parent = program_td.find_element(By.XPATH, "..")
antCompleteDate_td = driver.find_element(By.XPATH, '//*[@id="StudentTable"]/tbody/tr[3]/td/table/tbody/tr[3]')
antCompleteDate_parent = antCompleteDate_td.find_element(By.XPATH, '//*[@id="StudentTable"]/tbody/tr[3]/td/table/tbody/tr[3]')
advisor_body = driver.find_element(By.XPATH, '//*[@id="StudentTable"]/tbody/tr[4]/td')
advisor_lines = (advisor_body.text).split('\n')
advisor_lines_length = len(advisor_lines)
advisor_parent = advisor_lines[14]
class_level = advisor_lines[15]

# Your name and student id
student_Name = studentName.text
new_student_Name = student_Name.replace("Student:", "Name:\t\t\t\t")
updated_student_Name = new_student_Name.split("(")[0].strip()
studName = new_student_Name.replace(new_student_Name, updated_student_Name)
# very blunt way of removing the titles before the name
try:
   new_studName = studName.replace("Mr. ", "").replace("Mrs. ", "").replace("Ms. ", "")
except:
   pass
print(new_studName)

#Program and Catalog
program = program_parent.text
new_program = program.replace("Program:", "Program:\t\t\t")
print(new_program)

#Anticipated Completion Date
antCompleteDate = antCompleteDate_parent.text
new_antCompleteDate = antCompleteDate.replace("Date:", "Date:\t")
updated_antCompleteDate = new_antCompleteDate.replace("Anticipated\n", "Anticipated ")
print(updated_antCompleteDate)

#Advisor
new_advisor_parent = advisor_parent.replace("Advisor:", "Advisor:\t\t\t")
print(new_advisor_parent)

#Class Level
new_class_level = class_level.replace("Level:", "Level:\t\t\t")
print(new_class_level)

soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
child_in_prog = soup.find_all('b', {'class' : 'StatusOthers'})
child_not_started = soup.find_all('b', {'class' : 'StatusNotStarted'})

#Graduation requirements that are "In Progress" (not individual classes)
print("\n============  In Progress ============")
# gets the parent tags to see what sections status
for item in child_in_prog:
    parent_in_prog = item.parent
    text = parent_in_prog.text
    if 'Electives:' in text and '(Pending completion of unfinished activity)' in text:
        text = text.replace('\n', '')
    text = text.replace('(Pending completion of unfinished activity)', '')
    print('Section - ' + text)
print("============================================")

#Graduation requirements that are "Not Started" (not individual classes)
print("\n============  Not Started ============")
for item in child_not_started:
   parent_not_started = item.parent
   text = parent_not_started.text
   if 'Electives:' in text and '(Not started)' in text:
      text = text.replace('\n', '')
   text = text.replace('(Not started)', '')
   print('Section - ' + text)
print("============================================")

#Credits earned at 200+ level (out of 54 required)
higherCredits = audit_table.find_element(By.XPATH, 
   '/html/body/div/div[2]/div[4]/div[3]/table/tbody/tr[8]/td/table[6]/tbody/tr/td/table[2]/tbody/tr[2]/td')
print('(out of 54 req) 200+ level ' + higherCredits.text)

#Total credits earned (out of 120 required)
totalCredits = audit_table.find_element(By.XPATH, 
   '/html/body/div/div[2]/div[4]/div[3]/table/tbody/tr[8]/td/table[7]/tbody/tr/td/table[2]/tbody/tr[2]/td')
print('(out of 120 req) Total ' + totalCredits.text)

pdf_html = driver.page_source
if savePDF == True:
   saveToPDF(pdf_html)
elif savePDF == False:
   pass

# Successful Retrieval should be like:
# Academic Audit Summary
# ======================
# Name: 		Larlos Cargo (1100841)
# Program:	BA Computer Science (CS.BA)
# Catalog:	C2021
# Anticipated Completion Date:	05/15/23
# ...
# ...
