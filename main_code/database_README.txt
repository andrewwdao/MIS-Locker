For admin:
In order to use database for other system, copy file database.db to your desired SQL system

In order to see information from the database within the terminal, get the terminal to this folder, 
start a python shell by typing: python3

When inside the shell, copy the below and pass in terminal to start viewing or modifying the database
(please have a look at database.py to know which function to use)

*----start python script----*

from database import Database
dtb = Database()

dtb.getAllUserInfo()

*----end python script----*

now you can freely see or modify information of any member.


(c) 2020 Can Tho University