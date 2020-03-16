For admin:
In order to see information from the database within the terminal, get the terminal to this folder, 
start a python shell by typing: python3

When inside the shell, copy the below and pass in terminal to start viewing or modifying the fingerPrint sensor
(please have a look at fingerPrint.py to know which function to use)

*----start python script----*

import fingerPrint

fingerPrint.begin()
fingerPrint.activate()


*----end python script----*

now you can freely see or modify information of any member.


(c) 2020 Can Tho University