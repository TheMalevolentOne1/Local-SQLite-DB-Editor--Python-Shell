import re
import os

#Notes for development: Make the SQL Exportable and saveable in a file so that users can export the SQL statements generated by the program for documentation and report.


print("Welcome to the SQLite Local Database editor! \nYou should know who this was made by obvs :P")

userRequest = "" #assigning userRequest here to avoid later if statement checks in case of no database files.
isNotNull = ""

filePath = os.listdir()
for i in range(len(filePath)):
    if re.search(".db", filePath[i]):
        userRequest = str(input(f"A Database File has been found.\n\nYes or No is the file {filePath[i]} the correct database?: ")).title()
        if userRequest == "Yes":
            database = filePath[i]
            break
        elif userRequest != "Yes" and userRequest != "No":
            print("Answer provided was invalid. Input given processed as \"No\"")
        
if userRequest == "No":
    print("The database that you want has not been discovered. Please ensure that you have moved your database to the same file as this program and try again. \nThanks!")
    quit()

elif userRequest != "Yes":
    print("No database was found. Please ensure that you have moved your database to the same file as this program and try again.\nThanks!")
    quit()

import sqlite3

con = sqlite3.connect(database)
cur = con.cursor()

while True:
    sel = int(input("\nSQLite Database Editor Menu:\n\nPlease select one of the following options:\n1) Table Options\n2) Query Options\n3) Export Settings\n4) Quit\n\nWhat do you want to do: "))
    if sel == 1:
        tabMenu = False
        while not tabMenu:
            tabSel = int(input("Please select the table option you want: \n1) Create Table\n2) Drop Table\n3) Insert into table \n4) Alter a table \n5) View Existing Tables\n\nWhat do you want to do: "))
            if tabSel == 1:
                print("\nFor the table name please note that any whitespace will be removed i.e spaces, and it will be converted to standard naming unless it has already been specified i.e tbl")
                nameOfTable=str(input("Please enter the name you want this table to be called?: "))
                if nameOfTable[0:3] != "tbl":
                    nameOfTable = "tbl" + nameOfTable
                createTable = f"CREATE TABLE \"{nameOfTable}\" ( "
                numOfFieldsValid = False
                while not numOfFieldsValid:
                    try:
                        numOfFields=int(input("Please enter the number of fields you want the table to have?: "))
                    except ValueError:
                        print("The number of fields can only be a number")
                for i in range(numOfFields):
                    nameOfField = str(input("\nPlease enter the name you want to call the field: "))
                    dataTypeValid = False
                    while not dataTypeValid:
                        print("Currently Permitted Datatypes:\nTEXT\nINT\nDATE")
                        dataType = input("Please enter the datatype that this field should be: ").upper()
                        if dataType == "TEXT" or dataType == "INT" or dataType == "DATE":
                            dataTypeValid = True
                        else:
                            print("Invalid Datatype") 
                    print("The next few questions require Yes or No answers")
                    isPrimaryValid = False
                    while not isPrimaryValid:
                        isPrimary = input("Is this field a primary key?: ").title()
                        if isPrimary == "Yes" or isPrimary == "No":
                            isPrimaryValid = True
                        else:
                            print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        isUniqueValid = False
                        while not isUniqueValid:
                            isUnique = input("Is this field unique? (Not permitting duplicates): ").title()
                            if isUnique == "Yes" or isUnique == "No":
                                isUniqueValid = True
                            else:
                                print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        isNotNullValid = False
                        while not isNotNullValid:
                            isNotNull = input("Should this field allow null (Empty) values: ").title()
                            if isNotNull == "Yes" or isNotNull == "No":
                                isNotNullValid = True
                            else:
                                print("Invalid. Please enter Yes or No")
                    #Include Foreign Key Here as function call. Add later.
                    createTable += f"\"{nameOfField}\" {dataType}"
                    if isPrimary == "Yes":
                        createTable += " " + "PRIMARY KEY"
                    if isPrimary == "No" and isUnique == "Yes":
                        createTable += " " + "UNIQUE"
                    if isNotNull == "Yes":
                        createTable += " " + "NOT NULL"
                    if i+1 != numOfFields:
                        createTable += ", "
                    #Add Foreign Key at the end before the closing bracket

                    elif i+1 == numOfFields:
                        createTable += " " + ");"
                try:
                    result = cur.execute(createTable).fetchall()
                except sqlite3.OperationalError:
                    print("Table fields can not have the same name!") 
            if tabSel == 5:
                tables = cur.execute("SELECT * FROM sqlite_master WHERE type = \"table\"").fetchall()
                if len(tables) == 0:
                    print("This database has no tables!")
                else:
                    print(tables)
            else: 
                print("Invalid Option")
    else:
        print("Invalid Option")