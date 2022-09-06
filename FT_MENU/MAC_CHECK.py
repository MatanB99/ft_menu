#!/bin/env python


import re, subprocess


mac_of_card = ''
mac_of_user = ''
next_mac = ''


def user_mac_input(mac_user, offset):
        add_offset = int(mac_user.replace('',''), 16) + offset # turns mac to int and adds offset
        global next_mac
        next_mac = ":".join(re.findall("..", "%012x"%add_offset)) # returs the next mac
        global mac_of_user
        mac_of_user = mac_user


def find_mac_of_card(bus_num, ven_id):
    bus = list(subprocess.check_output("lspci -n |grep " + f'{ven_id}'+ " |awk {'print $1'} ", shell=True).decode().splitlines())
    portname = subprocess.check_output("lshw -businfo |grep " + bus[bus_num] + " |awk '{print $2}'", shell=True).decode().strip()
    with open("/sys/class/net/" + f'{portname}' + "/address") as f:
        global mac_of_card
        mac_of_card = f.read().strip().upper()


def mac_compare(ven_id_input, mac_user_input):
    portamount = subprocess.check_output("lspci -n |grep " + f'{ven_id_input}' + "| wc -l ", shell=True)
    find_mac_of_card(bus_num=0, ven_id=ven_id_input)
    mac_of_card_int = mac_of_card.replace(":", "")
    test = ''
    check = 'MAC Adrresses of card: \n'
    if re.match(mac_user_input, mac_of_card_int, re.I):
        for x in range(0, int(portamount)):
            user_mac_input(mac_user=mac_user_input, offset=x)
            find_mac_of_card(bus_num=x, ven_id=ven_id_input)
            if re.match(next_mac, mac_of_card, re.I):
                test = "PASS MAC"
            else:
                test = "FAIL MAC"
            check = check + mac_of_card + " \n"
        print(test)
        return check
    else:
        mac_not_match = "MAC of user does not match first MAC of card"
        print(mac_not_match)
        return mac_not_match


if __name__ == '__main__':
    mac_compare()
