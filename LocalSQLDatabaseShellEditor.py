import re
import os

export = False
warning = ""


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

print("Notice: if you would like the SQL to be exported to a file for documentation purposes please enable it inside of the ")

while True:
    sel = int(input("\nSQLite Database Editor Menu:\n\nPlease select one of the following options:\n1) Table Options\n2) Query Options\n3) Export Settings\n4) Quit\n\nWhat do you want to do: "))
    if sel == 1:
        tabMenu = False
        while not tabMenu:
            tabSel = int(input("Please select the table option you want: \n1) Create Table\n2) Drop Table\n3) Insert into table \n4) Edit a Table \n5) View Existing Tables\n6) Back\n\nWhat do you want to do: "))
            if tabSel == 1:
                print("\nFor the table name please note that any whitespace will be removed i.e spaces, and it will be converted to standard naming unless it has already been specified i.e tbl")
                nameOfTableValid = False
                primaryKeys=[]
                while not nameOfTableValid:
                    nameOfTable=str(input("Please enter the name you want this table to be called?: "))
                    if nameOfTable == "":
                        print("A table name has not been entered")
                    else:
                        nameOfTableValid = True
                if nameOfTable[0:3] != "tbl":
                    nameOfTable = "tbl" + nameOfTable
                createTable = f"CREATE TABLE \"{nameOfTable}\" ( "
                numOfFieldsValid = False
                while not numOfFieldsValid:
                    try:
                        numOfFields=int(input("Please enter the number of columns you want the table to have?: "))
                        break
                    except ValueError:
                        print("The number of columns can only be a number")
                for i in range(numOfFields):
                    nameOfField = str(input("\nPlease enter the name you want to call the column: "))
                    dataTypeValid = False
                    while not dataTypeValid:
                        print("Currently Permitted Datatypes:\nTEXT\nINT\nDATE")
                        dataType = input("Please enter the datatype that this column should be: ").upper()
                        if dataType in ['TEXT','INT','DATE']:
                            dataTypeValid = True
                        else:
                            print("Invalid Datatype") 
                    print("The next few questions require Yes or No answers")
                    isPrimaryValid = False
                    while not isPrimaryValid:
                        isPrimary = input("Is this column a primary key?: ").title()
                        if isPrimary in ['Yes','No']:
                            isPrimaryValid = True
                        else:
                            print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        isUniqueValid = False
                        while not isUniqueValid:
                            isUnique = input("Is this column unique? (Not permitting duplicates): ").title()
                            if isUnique in ['Yes','No']:
                                isUniqueValid = True
                            else:
                                print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        isNotNullValid = False
                        while not isNotNullValid:
                            isNotNull = input("Should this column allow null (Empty) values: ").title()
                            if isNotNull in ['Yes','No']: 
                                isNotNullValid = True
                            else:
                                print("Invalid. Please enter Yes or No")
                    #Include Foreign Key Here as function call. Add later.
                    createTable += f"\"{nameOfField}\" {dataType}"
                    if isPrimary == "Yes":
                        primaryKeys.append(nameOfField)
                    if isPrimary == "No" and isUnique == "Yes":
                        createTable += " " + "UNIQUE"
                    if isNotNull == "Yes":
                        createTable += " " + "NOT NULL"
                    
                    createTable += ", "
                    print(primaryKeys)
                    #Add Foreign Key at the end before the closing bracket

                    if i+1 == numOfFields:
                        createTable += " PRIMARY KEY ( "
                        for i in range(len(primaryKeys)):
                            createTable += f"\"{primaryKeys[i]}\""
                            if i+1 != len(primaryKeys):
                                createTable += ", "
                        createTable += " )"
                        createTable += " " + ");"
                primaryKeys = []

                try:
                    cur.execute(createTable)
                    print("Table was successfully created!")
                except sqlite3.OperationalError as err:
                    if re.search("already exists", str(err)):
                        print(f"A table with the name {nameOfTable} already exists :(")
                    elif re.search("duplicate column name", str(err)):
                        print("Tables can not have duplicate column names!")
                    else:
                        raise
            elif tabSel == 2:
                print("")
            elif tabSel == 3:
                print("")
            elif tabSel == 4:
                print("")
            elif tabSel == 5:
                tableList = []
                for i in cur.execute("SELECT * FROM sqlite_master WHERE type = \"table\""):
                    tableList.append(i)
                print(tableList)
            else:
                print("Invalid Option")
    elif sel == 3:
        try:
            setSel = int(input(f"1) Export: {export} 2) Set Export file\n\nWhat would you like to do?: "))
            if setSel == 1:
                status = ""
                if export == True:
                    status = "disable"
                else:
                    status = "enable"
                while warning not in [True,False]:
                    warning = bool(input("Warning: Are you sure you want to active exports: ")).title()
                    if warning not in [True,False]:
                        print("Only acceptable values are true and false!")
                exports = warning
        except ValueError:
            print("Must be a number!")
    else:
        print("Invalid Option")