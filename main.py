from bs4 import BeautifulSoup
from selenium import webdriver
import csv

offline = True
soup = None
transferColleges = transferClassesTables = []

if offline == True:
    file = open("MCCtoNJIT.html","r")
    contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')
else:
    #webscraping stuff that i cant get to work (havent used selenium before)
    #driver = webdriver.Chrome()
    #NJtransferURL = 'https://njtransfer.org/artweb/listeqs.cgi?MI+NI'
    #driver.get(NJtransferURL)
    #click button and get html
    pass

transferClassesTables.append(soup.find('table'))
classEquivalencyTable = transferClassesTables[0]

#classEquivalencyTable = soup.find('table') #extracting just the table from site

# Using readlines() to grab all the lines in the text file
CCclasses = open('CCclasses.txt', 'r') #txt file that has every class taken at CC on a separate line (grabbed from CC website)
CCclasses = CCclasses.readlines()

file = open('output.csv', 'w')
writer = csv.writer(file)
writer.writerow(['CC class', 'CC class name', 'Transfer class', 'comments']) #create CSV file

for CCclass in CCclasses:

    #if (line.find("Elective") and line.find("OR") and line.find("Semester") == -1): #putting it into 1 line is not working as expected, going to use a lot of if statements
    if(CCclass.find("Semester") != -1): #filtering to only have the class
        continue   
    elif(CCclass.find("Elective") != -1):
        continue 
    elif(CCclass.find("OR") != -1):
        continue 
    
    CCclass = CCclass.strip() #preprocessing so it is ready to check with table
    CCclass = CCclass.replace("-","") 
    
    potentialEquivalents = classEquivalencyTable.findAll("a", string=CCclass)
    for equivalent in potentialEquivalents:
        attributes = equivalent.parent.parent.findAll("td")
        CCclassName = attributes[2].text.strip()
        transferClass = attributes[5].text.strip()
        comment = attributes[6].text.strip()

    
    writer.writerow([CCclass, CCclassName, transferClass, comment])

file.close() 
    
    
