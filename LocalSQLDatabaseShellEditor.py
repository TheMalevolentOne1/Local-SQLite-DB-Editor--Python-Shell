import re
import os

export = False
warning = ""
file = ""

print("\n\nWelcome to the SQLite editor!\nYou should know who this was made by :P \nIf you would like the SQL to be exported please go to the export settings.")

userRequest = ""
isNotNull = ""
database = ""

while True:
    newOrEx = str(input("Would you like to make a New or use an Existing database: ")).title()
    if newOrEx not in ['New','Existing']:
        print("New or Existing are the only acceptable values")
    else:
        if newOrEx == "Existing":
            filePath = os.listdir()
            if len(filePath) == 0:
                print("No databases could be found!")
                quit()
            else:
                for i in range(len(filePath)):
                    if re.search(".db", filePath[i]):
                        print("A Database File has been found.")
                        while True:
                            userRequest = str(input(f"\nYes or No is the file {filePath[i]} the correct database?: ")).title()
                            if userRequest == "Yes":
                                database = filePath[i]
                                break
                            elif userRequest not in ['Yes','No']:
                                print("Invalid Answer.")
                            else:
                                break
                        if userRequest == "Yes":
                            break
                if database != "":
                    break
        elif newOrEx == "New":
            while True:
                nameDB = str(input("What do you want to call the new database?: "))
                try:
                    open(nameDB+".db","x")
                    database = f"{nameDB}.db"
                    break
                except:
                    raise
            break
        else:
            print("Invalid Option")
            
if userRequest == "No":
    print("The database that you want has not been discovered. Please ensure that you have moved your database to the same file as this program and try again. \nThanks!")
    quit()
    

import sqlite3

con = sqlite3.connect(database)
cur = con.cursor()

while True:
    try:
        sel = int(input("\nSQLite Database Editor Menu:\n\nPlease select one of the following options:\n1) Table Options\n2) Query Options\n3) Export Settings\n4) Quit\n\nWhat do you want to do: "))
    except ValueError:
        print("That was not a number :)")
    if sel == 1:
        tabMenu = False
        while not tabMenu:
            tabSel = 0
            try:
                tabSel = int(input("\nPlease select the table option you want: \n1) Create Table\n2) Drop Table\n3) Insert into table \n4) Alter a table \n5) View Existing Tables\n6) Back\n\nWhat do you want to do: "))
            except ValueError:
                print("Can only be a number :)")
            if tabSel == 1:
                print("\nFor the table name please note that any whitespace will be removed i.e spaces, and it will be converted to standard naming unless it has already been specified i.e tbl")
                primaryKeys=[]
                while True:
                    nameOfTable=str(input("Please enter the name you want this table to be called?: "))
                    if nameOfTable == "":
                        print("A table name has not been entered")
                    else:
                        break
                if nameOfTable[0:3] != "tbl":
                    nameOfTable = "tbl" + nameOfTable
                createTable = f"CREATE TABLE \"{nameOfTable}\" ( "
                while True:
                    try:
                        numOfFields=int(input("\nPlease enter the number of columns you want the table to have?: "))
                        break
                    except ValueError:
                        print("The number of columns can only be a number")
                for i in range(numOfFields):
                    nameOfField = str(input("\nPlease enter the name you want to call the column: "))
                    while True:
                        print("Currently Permitted Datatypes:\nTEXT\nINT\nDATE")
                        dataType = input("\nPlease enter the datatype that this column should be: ").upper()
                        if dataType in ['TEXT','INT','DATE']:
                            break
                        else:
                            print("Invalid Datatype") 
                    print("The next few questions require Yes or No answers")
                    while True:
                        isPrimary = input("Is this column a primary key?: ").title()
                        if isPrimary in ['Yes','No']:
                            break
                        else:
                            print("Invalid. Please enter Yes or No")
                    while True:
                        isForeign = input("Is this column a foreign key?: ").title()
                        if isForeign == "Yes":
                            tableReference = input("What table do you want this column to act as a foreign key for?: ")
                            columnReference = input(f"What column in the {tableReference} do you want to act the foreign key for?: ")
                            try:
                                cur.execute(f"SELECT {columnReference} FROM {tableReference}")
                            except sqlite3.OperationalError as err:
                                if re.search("no such table", err):
                                    print(f"The {tableReference} does not exist!")
                                else:
                                    raise
                        elif isForeign == "No":
                            break
                        else:
                            print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        while True:
                            isUnique = input("Is this column unique? (Not permitting duplicates): ").title()
                            if isUnique in ['Yes','No']:
                                break
                            else:
                                print("Invalid. Please enter Yes or No")
                    if isPrimary != "Yes":
                        while True:
                            isNotNull = input("Should this column allow null (Empty) values: ").title()
                            if isNotNull in ['Yes','No']: 
                                break
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
                    result = cur.execute(createTable)
                    print("\nTable Successfully Created!")
                    if export == True:
                        with open(file, "a") as f:
                            f.write(createTable)
                            f.close()
                except sqlite3.OperationalError as err:
                    if re.search("already exists", str(err)):
                        print(f"A table with the name {nameOfTable} already exists")
                    elif re.search("duplicate column name", str(err)):
                        print("Tables can not have duplicate column names!")
                    else:
                        raise

            elif tabSel == 2:
                dropTable = str(input("Please enter the table name you wish to drop: "))
                try:
                    cur.execute(f"DROP TABLE \"{dropTable}\"")
                    print("\nTable successfully Deleted!")
                    if export == True:
                        with open(file, "a") as f:
                            f.write(f"\nDROP TABLE \"{dropTable}\"")
                            f.close()
                except sqlite3.OperationalError as err:
                    if re.match("no such table",str(err)):
                        print(f"A table with the name {dropTable} does not exist.")
                    else:
                        raise
            elif tabSel == 3:
                print("")
            elif tabSel == 4:
                print("")
            elif tabSel == 5:
                tableSQL = []
                tableData = []
                for i in cur.execute("SELECT * FROM sqlite_master WHERE type = \"table\""):
                    tableSQL.append(i[4])

                if tableSQL == []:
                    print("\nThis Database has no tables!")
                else:
                    for i in tableSQL:
                        arr = i.split(" ")
                        #Getting Table Names
                        tableData.append(arr[arr.index("TABLE")+1])
                        print(arr[arr.index("TABLE")+1])
                    print("Existing Tables:")
                    for i in tableData:
                        print(f"Table Name: {i}")
                    
            elif tabSel == 6:
                tabMenu = True
            else:
                print("Invalid Option")

    elif sel == 3:
        try:
            setSel = int(input(f"1) Export: {export} \n\nWhat would you like to do?: ")) #Add additional options at a     
            if setSel == 1:
                status = ""
                if export == True:
                    status = "disable"
                else:
                    status = "enable"
                while True:
                    warning = str(input(f"Warning: Are you sure you want to try to {status} exports: ")).title()
                    if warning not in ["Yes","No"]:
                        print("Only acceptable values are Yes and false!")
                    else:
                        break

                if warning == "Yes" and export == False:
                    while True:
                        fileChoice = str(input("\nDo you want to create a new file or would you like to use existing? \nPlease type Existing or New: ")).title()
                        if fileChoice in ['Existing','New']:
                            break
                        else:
                            print("Only Existing or New are valid.")
                    if fileChoice == "New":
                        fileName = str(input("\nWhat do you want to call the file: "))
                        try:
                            open(fileName+".txt", "x")
                            file = open(fileName+".txt", "w")
                            print(f"\n{fileName} was chosen as the text file to export to.")
                            export = True
                        except FileExistsError as err:
                            print("This file already tests")
                    elif fileChoice == "Existing":
                        filePath = os.listdir()
                        for i in filePath:
                            if re.search(".txt",str(i)):
                                txtCheck = ""
                                while True:
                                    txtCheck = str(input(f"is {i} the text file that you want to export to: ")).title()
                                    if txtCheck in ['Yes','No']:
                                        break
                                    else:
                                        print("Only yes or no are acceptable values")
                            try:
                                if txtCheck == "Yes":
                                    file = i
                                    export = True
                                    print(f"\n{i} was chosen as the text file to export to.")
                                    break
                            except NameError:
                                if filePath.index(i) + 1 == len(filePath):
                                    txtCheck = None
                                    print("No text file was found")
                elif warning == "Yes" and export == True:
                    file = ""
                    export = False
                    print("Exporting has been disabled.")
        except ValueError:
            print("Must be a number!")
    elif sel == 4:
        quit()
    else:
        print("Invalid Option")
