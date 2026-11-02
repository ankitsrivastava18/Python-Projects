# creating a file
#1. mode -> x - creates a file
# open('diwali.txt','r') 

#2. mode -> w - creates a file and you can write inside that file
# file = open('navratri.txt','w')
# file.write('garba khelo din raat khelo')
# file.write('din bhar padhai karo ho jayega') # overiding

# file = open('navratri.txt','a')
# file.write('\npresentation acchi rakho ho jayega')

# file.close()

# # deleting the file
# from pathlib import Path
# import os
# p = Path('navratri.txt')
# os.remove(p) 

# another way of opening and working with a file

# with open('diwali.txt','a') as fs:
#     fs.write('hello')  

# next day

from pathlib import Path
import os
import shutil

def create_folder():
    fol_name = input("tell the name of your folder : ")
    p = Path(fol_name) 
    if p.exists():
        print("folder already exist try again ")
        create_folder()
    else:
        p.mkdir()
        print("New folder created successfully! ")  

def read_folder():
    p = Path("")
    items = list(p.rglob("*"))

    for i in range(len(items)):
        print(f"{i+1} : {items[i]}")    

def update_folder():
    read_folder()
    fol_name = input("which folder you want to update :-")
    old_p = Path(fol_name)

    if old_p.exists():
        new_name = input("Enter your new name :-") 
        new_p = Path(new_name) 
        old_p.rename(new_name)
        print("updated")

    else:
        print("name does not exist try again ") 
        update_folder()

import shutil
from pathlib import Path

def delete_folder():
    read_folder()
    fol_name = input("tell the name of your folder : ")
    p = Path(fol_name)

    if not p.exists() or not p.is_dir():
        print("folder doesn't exist try again ")
        delete_folder()
    else:
        confirm = input(f"'{fol_name}' and everything inside it will be deleted. Are you sure? (y/n) :- ")
        if confirm.lower() == "y":
            shutil.rmtree(p)
            print("Folder deleted successfully! ")
        else:
            print("Deletion cancelled") 

def create_file():
     name = input("tell your file name with extension :-") 
     p = Path(name)
     if p.exists() and p.is_file():
          print("file name already exist please try again") 
          create_file() 
     else:
          with open(p,'w') as fs:
               data = input("what do you want to write :-")
               fs.write(data)
               print("file is created successfully")  

def read_file():
     items = read_folder()
     for i in items:
          p = Path(i) 
          if p.is_file():
               print(i) 

     name = input("which file you wnat to read :-")
     p = Path(name)
     if p.exists() and p.is_file():
          with open(p,"r") as fs:
               data = fs.read()
               print("\n\n\nyour file content is \n\n\n")
               print(data)

     else:
          print("no such file exist please try again")
          read_file()                     
        #   i = str(i)
        #   for j in i:
        #        if j == ".":
        #             print(i)
        #             break                         

def update_file():
     items = read_folder()
     for i in items:
        p = Path(i) 
        if p.is_file():
            print(i) 

     name = input("Tell your file name :- ")
     p = Path(name)
     if p.exists() and p.is_file():
                 
        print("choose one of the option")
        print("press 1 to change the name")
        print("press 2 to overwrite the file content")
        print("press 3 to append new content")

        res = int (input("tell your response :-"))

        if res == 1:
             new_name = input("tell new name with extension")
             new_p = Path(new_name)
             p.rename(new_p)
             print("file name changed successfully ")

        elif res == 2:
             with open(p,'w') as fs:
                  data = input("what do you want to overwrite:-")
                  fs.write(data)
                  print("overwrite successfully")

        elif res == 3:
             with open(p,'a') as fs:
               data = input("what do you want to append:-")
               fs.write(data)
               print("Append successfully")

def delete_file():
     items = read_folder()
     for i in items:
        p = Path(i) 
        if p.is_file():
            print(i) 

        name = input("tell name of your file with extension :-")
        p = Path(name)
        if p.exists() and p.is_file():
            os.remove(p)
        else:
            print("no such file exist")
            delete_file()                  
                            

print('press 1 - for creating a folder')
print('press 2 - for reading a folder')
print('press 3 - for updating a folder')
print('press 4 - for deleting a folder')
print('press 5 - for creating a file')
print('press 6 - for reading a file')
print('press 7 - for updating a file')
print('press 8 - for deleting a file')

res = int(input("Tell Your Response :-")) 

if res == 1:
    create_folder() 

if res == 2:
    read_folder()

if res == 3:
    update_folder()


if res ==4:
    delete_folder() 

if res == 5:
        create_file() 

if res == 6:
     read_file()        

if res == 7:
     update_file()      

if res == 8:
     delete_file()     