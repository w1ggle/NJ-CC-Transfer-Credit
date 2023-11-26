# Using readlines() to grab all the lines in the text file
file1 = open('CCclasses.txt', 'r') #txt file that has every class taken at CC on a separate line (grabbed from CC website)
Lines = file1.readlines()
 
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
    #print(line) #classes are preprocessed and ready to compare for webscraping
    
    
