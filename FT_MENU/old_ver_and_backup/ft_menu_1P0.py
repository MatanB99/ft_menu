#!/usr/bin/env python

# author - Matan Bathan
# matanb@silicom.co.il
# Current Ver.: 1.0
# Changes: 
# Ver. 1.0 - release ver.

import PCI_CHECK, MAC_CHECK, FRU_CHECK
import subprocess
from re import search
from datetime import date


"""
# for practice:
# f4:8e:38:c5:96:7c mac pizza
# 14e4:165f ven id pizza
# 8086:1591 ven id sts4
# 8086:1592 ven id sts3
# 8086:0d5c ven id lisbon2
# 1000:c010 ven id LBG x9
# 8086:37c0 ven id LBG x2
"""


def usb_test():
    lsusb = str(subprocess.check_output("lsusb", shell=True).decode())
    lsusb_result = "USB TEST: \n"
    USB = "1374:0001"
    UBLOX = "1546:01a9"
    if search(USB, lsusb) and search(UBLOX, lsusb):
        USB_OUTPUT = str(subprocess.check_output("lsusb |grep 1374:0001", shell=True).decode())
        UBLOX_OUTPUT = str(subprocess.check_output("lsusb |grep 1546:01a9", shell=True).decode())
        lsusb_result += USB_OUTPUT + UBLOX_OUTPUT + "\n"
        print("PASS USB")
        return lsusb_result
    else:
        lsusb_result += "FAILED USB CHECK: \n" + lsusb
        print(lsusb_result)
        return lsusb_result


def pizza():
    print("you chose pizza")
    logname = str(input("Tracking: "))
    portnum = 4
    venid = "14e4:165f"
    pcispeed = 5
    pciwidth = 1
    macadrs = "f48e38c5967c" #str(input("mac adr: "))
    with open(logname + ".txt", "a+") as f:
        f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")
        f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n")
        f.write(str(MAC_CHECK.mac_compare(venid, macadrs)))
        f.close()
    

def sts4():
    print("you chose sts4")
    logname = str(input("Tracking: "))
    portnum = 12
    venid = "8086:1591"
    pcispeed = 8 #16 on gen4
    pciwidth = 8
    macadrs = str(input("mac adr: "))
    with open(logname + ".txt", "a+") as f:
        f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")
        f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n")
        f.write(usb_test())
        f.write(str(MAC_CHECK.mac_compare(venid, macadrs)))
        f.close()


def sts3():
    print("you chose sts3")
    logname = str(input("Tracking: "))
    portnum = 8
    venid = "8086:1592"
    pcispeed = 8
    pciwidth = 8
    macadrs = str(input("mac adr: "))
    with open(logname + ".txt", "a+") as f:
        f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")
        f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n")
        f.write(usb_test())
        f.write(str(MAC_CHECK.mac_compare(venid, macadrs)))
        f.close()


def lisbon2():
    print("you chose lisbon2")
    logname = str(input("Tracking: "))
    portnum = 1
    venid = "8086:0d5c"
    pcispeed = 8
    pciwidth = 8
    with open(logname + ".txt", "a+") as f:
        f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")
        f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n")
        f.write(str(FRU_CHECK.main(1, logname)))
        f.close()


def lbg():
    print("you chose LBG")
    logname = str(input("Tracking: "))
    portnum = 9
    venid = "1000:c010"
    pcispeed = 16
    pciwidth = 16
    with open(logname + ".txt", "a+") as f:
        f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")
        f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n") # 9x
        f.write(PCI_CHECK.checkpci(2, "8086:37c0", 8, 16) + "\n") # 2x
        f.write(str(FRU_CHECK.main(2, logname)))
        f.close()


def menu():
    card = ''
    try:
        card = int(input("choose an option: \n"
                         "1 - Pizza card \n"
                         "2 - STS4 \n"
                         "3 - STS3 \n"
                         "4 - Lisbon2 \n"
                         "5 - LBG \n"
                         "Enter choice: "))
    except:
        print("Try again with number between 1 - 5")
    if card == 1:
        pizza()
    elif card == 2:
        sts4()
    elif card == 3:
        sts3()
    elif card == 4:
        lisbon2()
    elif card == 5:
        lbg()


if __name__ == '__main__':
    menu()
