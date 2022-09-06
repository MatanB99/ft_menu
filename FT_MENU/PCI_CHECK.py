#!/usr/bin/env python

# Artyom Serhiienko
# Ver. 1Pa
# Revision History:
# 1Pa - Alfa Version
# Checking speed and width PCIe

### Test Options ###
# PORT_NUM = 4 - Number Ports
# VEN_ID = "14e4:165f"  #Chip vendor ID
# OLD_PCI_SPEED = 5     #PCI SPEED (Exemple: 8, 16)
# OLD_PCI_WIDTH = 1     #PCI WIDTH (Exemple: 8, 16)
### Connect Module ###
# PCI_CHECK.checkpci(PORT_NUM,VEN_ID,OLD_PCI_SPEED,OLD_PCI_WIDTH)

####################################################################
###########         Module Check PCI
###########
###########
###########
####################################################################

#Start Import module

import re
import subprocess
from re import search


#CHIP_NAME = "BCM5720" #CARD CHIP NAME (Exemple: 810, X710)
#PORT_NUM = 4
#VEN_ID = "14e4:165f"  #Chip vendor ID
#OLD_PCI_SPEED = 5     #PCI SPEED (Exemple: 8, 16)
#OLD_PCI_WIDTH = 1     #PCI WIDTH (Exemple: 8, 16)


##################### CHECK PCI START #######################
def checkpci(PORT_NUM,VEN_ID,OLD_PCI_SPEED,OLD_PCI_WIDTH):
    #Port List
    global Portdict
    Portdict = []

    NEW_PCI_SPEED, NEW_PCI_WIDTH = f'{OLD_PCI_SPEED}GT', f'x{OLD_PCI_WIDTH}'

    output = "PCI DETECTION TEST - HOST\n"

    lspci = subprocess.check_output(["lspci -n |grep " + f'{VEN_ID}'], shell=True)

    total_occurrences = str(lspci).count(VEN_ID)
    output = output + "Found " + str(total_occurrences) + " Ports\n"
    if total_occurrences >= PORT_NUM:
        output = output + "PASS - All " + f'{PORT_NUM}' + " Ports " + f'{VEN_ID}' + " Detected On Host\n"
    else:
        output = output + "FAILED - Not All " + f'{VEN_ID}' + " Detected On Host\n"

    output = output + "PCI SPEED & WIDTH TEST - HOST | LINK DETECTED & SPEED\n"

    lbg_speed = f'{8}GT'

    #List Bus create 
    lines = []
    lines = str(lspci).split('\\n')
    for x in range(PORT_NUM):
        if not lspci:
            output = output + "FAILED - Chip not found\n"
            break
        else:
            bus_all = (lines[x])
            bus = bus_all.split(' ', 1)[0]
            bus = bus.replace("b'", '')
        
        #PCI SPEED CHECK
        pci_sta = subprocess.check_output(["lspci -s " + f'{bus}' + " -vvv | grep LnkSta:"], shell=True)
        if VEN_ID=="1000:c010": #pci check for LBG
            if re.search(r''f'{NEW_PCI_SPEED}', f'{pci_sta}'):
                output = output + "PASS - For PCI Bus # " + f'{bus}' + "  : Speed is " + f'{NEW_PCI_SPEED}\n'
            elif re.search(r''f'{lbg_speed}', f'{pci_sta}'):
                output = output + "PASS - For PCI Bus # " + f'{bus}' + "  : Speed is " + f'{lbg_speed}\n'
            else:
                output = output + "FAILED - For PCI Bus # " + f'{bus}' + "  : Speed is not " + f'{NEW_PCI_SPEED}\n'
             #PCI WIDTH CHECK
            if re.search(r''f'{NEW_PCI_WIDTH}', f'{pci_sta}'):
                output = output + "PASS - For PCI Bus # " + f'{bus}' + "  : Width is " + f'{NEW_PCI_WIDTH}\n'
            else:
                output = output + "FAILED - For PCI Bus # " + f'{bus}' + "  : Width is not " + f'{NEW_PCI_WIDTH}\n'

        else: #pci check for not LBG
            if re.search(r''f'{NEW_PCI_SPEED}', f'{pci_sta}'):
                output = output + "PASS - For PCI Bus # " + f'{bus}' + "  : Speed is " + f'{NEW_PCI_SPEED}\n'
            else:
                output = output + "FAILED - For PCI Bus # " + f'{bus}' + "  : Speed is not " + f'{NEW_PCI_SPEED}\n'
            # PCI WIDTH CHECK
            if re.search(r''f'{NEW_PCI_WIDTH}', f'{pci_sta}'):
                output = output + "PASS - For PCI Bus # " + f'{bus}' + "  : Width is " + f'{NEW_PCI_WIDTH}\n'
            else:
                output = output + "FAILED - For PCI Bus # " + f'{bus}' + "  : Width is not " + f'{NEW_PCI_WIDTH}\n'

    pcifail = "FAIL"
    count_lbg_speed = output.count(lbg_speed)
    if VEN_ID=="1000:c010" and count_lbg_speed != 2:
        print(output)
        return output
    elif search(pcifail, output):
        print(output)
        return output
    else:
        print("PASS PCI")
        return output

##################### CHECK PCI END #######################

# Main
if __name__ == '__main__':
    checkpci()


