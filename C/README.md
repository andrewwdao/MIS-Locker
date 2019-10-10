THIS IS THE C CODES AND C COMPILED PROGRAMS USED TO CONTROL 6 74HC595 (2 PERIPHERAL MODULES OF THE MIS LOCKER).

peripheral_init can be call directly with: ./peripheral_init

HOWEVER, peripheral_main cannot be call like that, you have to put parameters on it:

Ex: ./peripheral_main 1 2 3 4 5 6

with 1 2 3 are 3 bytes you want to give the first module, and 4 5 6 are 3 bytes you want to give the second module.


(c) Minh-An Dao 2019
