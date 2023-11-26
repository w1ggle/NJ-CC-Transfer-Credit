# https://www.samsclub.com/robots.txt states that this should be fine to scrape their website. If a rep from Sam's Club wants me to remove it, feel free to contact me and I will remove this
# https://www.bjs.com/robots.txt states that this should be fine to scrape their website. If a rep from BJs wants me to remove it, feel free to contact me and I will remove this

from bs4 import BeautifulSoup
import requests
import csv
import re
from datetime import date























#get packages
print("Installing packages") 
setup.install()

#get html from website
print("Scraping URLs")  #TODO add if statement to check if we got a request, else print error
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/99.0", 
    "method": "GET"
}

microcenterURL = "https://www.microcenter.com/search/search_results.aspx?N=4294967288+4294818548+4294819270+4294819837+4294814254+4294814572+4294805366+4294814062+4294816439+4294818783&NTK=all&sortby=pricelow&rpp=96&storeID=075"
page_to_scrape = requests.get(microcenterURL,headers=headers) 
MicroSoup = BeautifulSoup(page_to_scrape.text, 'html.parser') 

passmarkURL = "https://www.cpubenchmark.net/cpu.php"
page_to_scrape = requests.get(passmarkURL,headers=headers)
PassSoup = BeautifulSoup(page_to_scrape.text, 'html.parser')


#tabulating
print("Tabulating data") 
file = open('output.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Brand', 'Model', 'CPU', 'CPU Score', 'RAM (GB)', 'RAM Type', 'Storage (GB)', 'GPU', 'Size (In)', 'Color', 'Price ($)', 'Refurbed' , 'Open Box', 'Link' ]) #create CSV file

products = MicroSoup.findAll('div', attrs={"class":"result_right"}) #extracting data from each product
for product in products: 
    brand = model = cpu = score = ramCapacity = ramType = storage = gpu = price = refurbishedStatus = openBoxStatus = color = size = link = None #gpu is usually None but did the rest for safety
        
    link = 'https://www.microcenter.com' + product.findAll("a")[1].get("href")
    brand = product.findAll("a")[1].get("data-brand") 
    model = product.findAll("a")[1].get("data-name") #example: ENVY x360 15-ey0013dx 15.6&quot; 2-in-1 Laptop Computer (Refurbished) - Black 

    index = model.rfind(' ')
    color = model[index+1:]
    
    if (model.find("Refurbished",index - 20) != -1):
        refurbishedStatus = "x"

    index = model.find(";")
    if(index == -1): #weird edge case for some laptop names
        index = model.find("-in-1")
    model = model[:index]

    index = model.rindex(" ")+1
    size = model[index:].replace('&quot','')
    model = model[:index]
    
    priceWrapper = product.find("div", attrs={"class":"price_wrapper"})
    priceOpenBox = priceWrapper.find("div", attrs={"class":"clearance"}) 
    priceOpenBoxIndex = priceOpenBox.text.find("$") 
    if (priceOpenBoxIndex != -1):
        price = (priceOpenBox.text[priceOpenBoxIndex:]) 
        openBoxStatus = "x"
    else:
        price = (priceWrapper.find("span", attrs={"itemprop":"price"}).text) 
    price = price.replace(',', '').replace('$', '') #remove $ sign and , so that it sorts correctly
    
    fullSpecs = product.find("div", attrs={"class":"h2"}).text.split("; ") #example: HP ENVY x360 Convertible 15-eu1073cl 15.6" 2-in-1 Laptop Computer (Refurbished) - Black;  AMD Ryzen 7 5825U 2.0GHz Processor;  16GB DDR4-3200 RAM;  512GB Solid State Drive;  AMD Radeon Graphics
    for spec in fullSpecs[1:]:
        if(spec.find("Processor") != -1):
            cpu = spec[:-9]
            if(cpu.find("AMD") != -1):
                cpu = cpu[5:]
            else:
                index = cpu.rindex("i")
                cpu = cpu[index:]
                cpu = re.sub(" ..th Gen ","-",cpu) 
            index = cpu.rfind(" ") 
            cpu=cpu[:index]
            index = cpu.rfind(" ") 
            if(index != -1 ): #weird case with ms surface not having processor Ghz in name
                cpu=cpu[:index] 
            score = PassSoup.find("a", string=re.compile(cpu)).parent.parent.findAll("td")[1].text.replace(",","")
        elif(spec.find("RAM") != -1):
            ram = spec[1:-4] 
            index = ram.find("GB")
            ramCapacity = ram[:index]
            ramType = ram[index+3:]
        elif(spec.find("Solid State Drive") != -1):
            storage = spec[:-18].replace("TB","000").replace("GB","")
        elif(spec.find("AMD") != -1 or spec.find("Intel") != -1 or spec.find("NVIDIA") != -1 ):
            gpu = spec

    writer.writerow([brand, model, cpu,score, ramCapacity, ramType, storage, gpu, size, color, price, refurbishedStatus, openBoxStatus, link]) #TODO see if its possible to get ALL inventory and not just 96 results, add my own personal score/rating, make csv 2 sheets where 1 is for calulations and other is for front end

file.close() 

today = date.today()

print("DONE! Check output.csv for prices as of " + today.strftime("%m/%d/%y"))