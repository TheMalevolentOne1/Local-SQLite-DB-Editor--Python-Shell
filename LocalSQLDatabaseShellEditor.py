import re
import sqlite3 as sql
import sys, os

print("Welcome to the SQLite Local Database editor! \n You should know who this was made by obvs :P")


filePath = os.listdir()
for i in range(len(filePath)):
    if re.search(".db", filePath[i]):
        userRequest = str(input(f"A Database File has been found.\n\nYes or No is the file {filePath[i]} the correct database?")).title()
        if userRequest == "Yes":
            i = len(filePath)
        elif userRequest != "Yes" and userRequest != "No":
            print("Answer provided was invalid. Input given processed as \"No\"")
        
if userRequest == "No":
    print("The database that you want has not been discovered. Please ensure that you have moved your database to the same file as this program and try again. \nThanks!")
    quit()

else:
    print("No database was found. Please ensure that you have moved your database to the same file as this program and try again.\nThanks!")
    

fE = False #fE = finished editing database :)

while not fE:
    

