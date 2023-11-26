from bs4 import BeautifulSoup
import requests
from selenium import webdriver

# Using readlines() to grab all the lines in the text file
file1 = open('CCclasses.txt', 'r') #txt file that has every class taken at CC on a separate line (grabbed from CC website)
Lines = file1.readlines()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/99.0", 
    "method": "GET"
}

NJtransferURL = 'https://njtransfer.org/artweb/listeqs.cgi?MI+NI'
#page_to_scrape = requests.get(NJtransferURL,headers=headers) 
#soup = BeautifulSoup(page_to_scrape.text, 'html.parser') 

#driver = webdriver.Chrome()
#driver.get(NJtransferURL)

file = open("MCCtoNJIT.html","r")
contents = file.read()
soup = BeautifulSoup(contents, 'html.parser')
classes = soup.find('table') #extracting data from each product

#print(classes)
for line in Lines:

    #if (line.find("Elective") and line.find("OR") and line.find("Semester") == -1): #putting it into 1 line is not working as expected, going to use a lot of if statements
    if(line.find("Semester") != -1): #filtering to only have the class
        continue   
    if(line.find("Elective") != -1):
        continue 
    if(line.find("OR") != -1):
        continue 
    
    line = line.strip()
    line = line.replace("-","") 
    
    equivalent = classes.findAll("a", string=line)
    print(equivalent)
    
    #print(line) #classes are preprocessed and ready to compare for webscraping
    
    
