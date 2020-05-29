# HARDWARE DOCUMENTATION

## SOURCE FILES AND EXPLANATION

Altium files of this project can be found on [pcb folder on github]

Detailed explanation can be found on my [undergraduate thesis report] (in Vietnamese only).

This file will only cover things that haven’t been mentioned on the thesis report.

## OPTO

After a long time using (6 months – 2 years), the electric locks may start to be warmed when working. If that happens, change the OPTO will solve the problem since the IR LEDs inside the OPTO are aging and cause the FET to not working properly.

## MOSFET

This project is using the Power MOSFET IRF540N as the main switch for the 12V LEDs and 12V solenoid locks.

However, this MOSFET is not ideally designed for switching application, it’s designed for linear mode operation.

Currently in the system, it operates in linear mode, but thanks to the high current and high voltage it can endure when applying 5V Vgs, it behaves like a switch.

But obviously this is not optimized design. Therefore, for further version of this system (if any), this type of MOSFET **is not recommended**. Switching type MOSFET is recommended (i.e.: [AO3400 SOT23-3 N-1CH 5A 30V])

## Buttons and limit switches

Button and limit switches in the system is first designed for using ADC converter in order to save GPIO pins. However, there are plenty of noises exist because of the low-profile power supply that could severely impact the ADC read. Therefore, ADC has been eliminated. GPIO digital interrupt reading has been used instead for reading buttons and switches. You can check out the Altium files to better understand what we have modified.

This method works well with 01 locker open, but with more than 01 locker open, it is not good since we cannot distinguish between them. In the future version, ADC or other methods could be used to distinguish between different limit switches of different lockers, but button should still be using interrupt digital read for stability.

<!-- Links -->
[pcb folder on github]: https://github.com/minhan74/MIS-Locker/tree/master/pcb
[undergraduate thesis report]: https://bit.ly/DMA_undergrad
[AO3400 SOT23-3 N-1CH 5A 30V]: https://icdayroi.com/ao3400-sot23-3-n-1ch-5a-30v