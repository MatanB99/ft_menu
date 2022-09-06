#!/usr/bin/python3.6
import datetime
import binascii
import subprocess
import os
import random
import sys
import time
import shutil

# from smbus2 import SMBus


# not included in python
def import_packages_that_are_not_included_in_python():
    """ Checks that all the packages that are not included in python are installed and imports them after """
    # package name as you would write if you type in cmd/terminal 'pip install package_name'
    packages_to_install = ["smbus2"]
    for package in packages_to_install:
        pip_check_if_package_installed_and_install_if_not(package)
    # import the packages after verifying that they are installed
    from smbus2 import SMBus
    global SMBus


# Constants
PYTHON_VERSION = "3.6"
# Colors
BLUE_COLOR = "\033[1;34;40m"
PURPLE_COLOR = "\033[1;35;40m"
YELLOW_COLOR = "\033[1;33;40m"
CYAN_COLOR = "\033[1;36;40m"
RED_COLOR = "\033[1;31;40m"
GREEN_COLOR = "\033[1;32;40m"
ALL_COLORS = [BLUE_COLOR, PURPLE_COLOR, YELLOW_COLOR, CYAN_COLOR, RED_COLOR, GREEN_COLOR]
RESET_STYLE_BLACK_BG = "\033[0;0;40m"
RESET_STYLE = "\033[0;0;0m"
# FRU
HEADER_STRING = b"TlvInfo\x00"
HEADER_VERSION = b"\x01"

""" v do not delete v
import practice
RUN_ON = int(practice.run_on_fru())
#while RUN_ON not in ["1", "2"]:
#    RUN_ON = input("Please Choose One Of The Following:\n"
#                   "1. Lisbon\n"
#                   "2. LGB\n")
RUN_ON = int(RUN_ON)
if RUN_ON == 1:
    FRU_ADDR = 0x53
    SILICOM_ONIE_VERSION = "R003"
elif RUN_ON == 2:
    FRU_ADDR = 0x51
    SILICOM_ONIE_VERSION = "R003"
else:
    print(RED_COLOR + "Unknown Mode" + RESET_STYLE_BLACK_BG)
    exit()
    """
#
HEX_TO_DECIMAL = {"0": 0,
                  "1": 1,
                  "2": 2,
                  "3": 3,
                  "4": 4,
                  "5": 5,
                  "6": 6,
                  "7": 7,
                  "8": 8,
                  "9": 9,
                  "a": 10,
                  "b": 11,
                  "c": 12,
                  "d": 13,
                  "e": 14,
                  "f": 15}
ALLOWED_CODES = ["21", "22", "23", "24", "25", "26", "27", "28", "29",
                 "2a", "2b", "2c", "2d", "2e", "2f", "fd", "fe"]
NOT_ALLOWED_CODES = ["00", "ff"]
CODES_MEANING = {"21": "Product Name: ",
                 "22": "Part Number: ",
                 "23": "Serial Number: ",
                 "24": "MAC: ",
                 "25": "Manufacture Date: ",
                 "26": "Device Version: ",
                 "27": "Label Revision: ",
                 "28": "Platform Name: ",
                 "29": "ONIE Version",
                 "2a": "Number Of MACs: ",
                 "2b": "Manufacturer: ",
                 "2c": "Country Code: ",
                 "2d": "Vendor: ",
                 "2e": "Diag Version: ",
                 "2f": "Service Tag: ",
                 "fd": "Vendor Extension: ",
                 "fe": "CRC-32 (checksum): "}


def pip_check_if_package_installed_and_install_if_not(name_of_package):
    """
    !! for python packages !!
    checks if name_of_package is installed and if not it installs it
    :param name_of_package: the name of the package to check if installed
                            name_of_package needs to be the same as if you would do 'pip install name_of_package'
    :type name_of_package: str
    """
    cmd = "python%s -m pip list" % PYTHON_VERSION
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if name_of_package not in output.decode():
        print(RED_COLOR + "'%s' not installed" % name_of_package + RESET_STYLE_BLACK_BG)
        print(GREEN_COLOR + "Proceeding To Installing '%s'" % name_of_package + RESET_STYLE_BLACK_BG)
        ok = False
        stop_when_zero = 4
        while not ok and stop_when_zero > 0:
            # ping google
            p = subprocess.Popen(["ping", "google.com", "-c4"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            if p.poll():
                print(RED_COLOR + "Please Connect The System To The Internet" + RESET_STYLE_BLACK_BG)
                input(CYAN_COLOR + "Press Enter When I'm Connected." + RESET_STYLE_BLACK_BG + "\n")
                print(GREEN_COLOR + "Checking Connection" + RESET_STYLE_BLACK_BG)
                try:
                    process = subprocess.Popen(["dhclient", "-r"], stdout=subprocess.PIPE)
                    process.wait()
                    time.sleep(2)
                    process = subprocess.run("dhclient -timeout 15".split(" "), stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, timeout=10)
                except subprocess.TimeoutExpired:
                    pass
            else:
                print(GREEN_COLOR + "Installing '%s'" % name_of_package + RESET_STYLE_BLACK_BG)
                cmd = "python%s -m pip install %s" % (PYTHON_VERSION, name_of_package)
                process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
                output, error = process.communicate()
                if "ERROR: No matching distribution found for %s" % name_of_package in output.decode():
                    print(RED_COLOR + "The Package '%s' Doesn't Exist." % name_of_package + RESET_STYLE)
                    exit()
                elif "Successfully installed" not in output.decode() and \
                        "Requirement already satisfied" not in output.decode():
                    print(RED_COLOR + "Failed To Install '%s'." % name_of_package + RESET_STYLE_BLACK_BG)
                    print(GREEN_COLOR + "Trying Again." + RESET_STYLE_BLACK_BG)
                    stop_when_zero -= 1
                else:
                    ok = True
                    print(GREEN_COLOR + "Successfully Installed '%s'." % name_of_package + RESET_STYLE_BLACK_BG)


def linux_check_if_package_installed_and_install_if_not(name_of_package):
    """
    !! for linux packages !!
    checks if name_of_package is installed and if not it installs it
    :param name_of_package: the name of the package to check if installed
                            name_of_package needs to be the same as if you would do 'yum install name_of_package'
    :type name_of_package: str
    """
    process = subprocess.Popen("sudo yum list installed".split(" "), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if "command not found" in output.decode():
        process = subprocess.Popen("apt list --installed".split(" "), stdout=subprocess.PIPE)
        output, error = process.communicate()
    if name_of_package not in output.decode():
        print(RED_COLOR + "'%s' not installed" % name_of_package + RESET_STYLE_BLACK_BG)
        print(GREEN_COLOR + "Proceeding To Installing '%s'" % name_of_package + RESET_STYLE_BLACK_BG)
        ok = False
        stop_when_zero = 4
        while not ok and stop_when_zero > 0:
            # ping google
            p = subprocess.Popen(["ping", "google.com", "-c4"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            if p.poll():
                print(RED_COLOR + "Please Connect The System To The Internet" + RESET_STYLE_BLACK_BG)
                input(CYAN_COLOR + "Press Enter When I'm Connected. " + RESET_STYLE_BLACK_BG + "\n")
                print(GREEN_COLOR + "Checking Connection" + RESET_STYLE_BLACK_BG)
                try:
                    process = subprocess.Popen(["dhclient", "-r"], stdout=subprocess.PIPE)
                    process.wait()
                    time.sleep(2)
                    process = subprocess.run("dhclient -timeout 15".split(" "), stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, timeout=10)
                except subprocess.TimeoutExpired:
                    pass
            else:
                print(GREEN_COLOR + "Installing '%s'" % name_of_package + RESET_STYLE_BLACK_BG)
                cmd = "sudo yum install %s -y" % name_of_package
                process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
                output, error = process.communicate()
                if "command not found" in output.decode():
                    cmd = "sudo apt-get install %s -y" % name_of_package
                    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                if "No package %s available." % name_of_package in output.decode():
                    print(RED_COLOR + "The Package '%s' Doesn't Exist." % name_of_package + RESET_STYLE)
                    exit()
                elif "Complete!" not in output.decode():
                    print(RED_COLOR + "Failed To Install '%s'." % name_of_package + RESET_STYLE_BLACK_BG)
                    print(GREEN_COLOR + "Trying Again." + RESET_STYLE_BLACK_BG)
                    stop_when_zero -= 1
                else:
                    ok = True
                    print(GREEN_COLOR + "Successfully Installed '%s'." % name_of_package + RESET_STYLE_BLACK_BG)


def scan_i2c_addresses():
    """
    Scans i2c Addresses And Return A List With All Active Addresses
    :return: list of active i2c addresses
    :rtype: list (of int)
    """
    p = subprocess.Popen("i2cdetect -l".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    i2c_addresses = []
    for address in range(0, 256):
        try:
            bus = SMBus(address)
            i2c_addresses.append(address)
            bus.close()
        except Exception:  # ignore exceptions as there will be an exception for each i2c address that isn't active
            pass
    return i2c_addresses


def get_i2c_bus_number_and_enable_access():
    """ checks what's the i2c bus number and return it """
    global i2c_bus_number
    # get i2c bus number
    i2c_addresses = scan_i2c_addresses()
    if len(i2c_addresses) == 1:
        i2c_bus_number = int(i2c_addresses[0])
    elif len(i2c_addresses) == 0:
        print(RED_COLOR + "Couldn't Find Active I2C Bus" + RESET_STYLE)
        exit()
    else:
        print("There Is More Then 1 Active I2C Bus.\n"
              "Please Chose The Desired Address.\n"
              "Available Addresses:\n"
              "%s\n\n" % (", ".join(i2c_addresses)))
        chosen_i2c_address = input("Address: ")
        try:
            chosen_i2c_address = int(chosen_i2c_address)
        except Exception:
            print(RED_COLOR + "PLease Enter Only Numbers." + RESET_STYLE_BLACK_BG)
            chosen_i2c_address = input("Address: ")
        while chosen_i2c_address not in i2c_addresses:
            print("Please Look Above For Active I2C Busses.\n")
            chosen_i2c_address = input("Address: ")
            try:
                chosen_i2c_address = int(chosen_i2c_address)
            except Exception:
                print(RED_COLOR + "PLease Enter Only Numbers." + RESET_STYLE_BLACK_BG)
        i2c_bus_number = int(chosen_i2c_address)


def output_fru_data_to_bin_file(fru_adr, file_name="onie_eeprom", verbose=True):
    """
    outputs the system fru to file_name.bin
    :param fru_adr:
    :param file_name: the name of the file that the data will be saved to, default is 'onie_eeprom' + '.bin'
                      file_name should be only the name with no extension.
    :param verbose: if verbose is True this func will print what it's doing, if verbose is False nothing will be printed
    :type file_name: str
    :type verbose: bool
    :return: the output file name, if there was a problem creating a file with the supplied file_name it will output
             the data to another file, so it returns the name of the output file.
    :rtype: str
    """
    FRU_ADDR = ''
    if fru_adr == 1:
        FRU_ADDR = 0x53
        SILICOM_ONIE_VERSION = "R003"
    elif fru_adr == 2:
        FRU_ADDR = 0x51
        SILICOM_ONIE_VERSION = "R003"
    global i2c_bus_number
    if file_name == "take system serial":
        file_name = "fru_" + datetime.datetime.now().strftime("%m.%d.%Y__%H_%M_%S")
    # open smbus to the i2c_bus_number
    bus = SMBus(i2c_bus_number)
    # read all the data in the fru
    fru_data = []
    #if verbose:
    #    print(GREEN_COLOR + "Reading From FRU" + RESET_STYLE_BLACK_BG)
    count_to_go_row_down = 64
    for i in range(0, 256):
        if count_to_go_row_down == 0 and verbose:
            count_to_go_row_down = 64
            print()
        try:
            byte = bus.read_byte_data(FRU_ADDR, i)
        except:
            print("please check deep switch")
            exit()
        #if verbose:
        #    print(ALL_COLORS[random.randint(0, len(ALL_COLORS) - 1)] + "-" + RESET_STYLE_BLACK_BG, end="")
        fru_data.append(byte)
        count_to_go_row_down -= 1
    if verbose:
        print()
    # close the smbus
    bus.close()
    # check if the len of fru_data is 10 or more
    # because if it is not it means the len of the entire fru data is missing and the data isn't valid
    if not len(fru_data) >= 10:
        print(RED_COLOR + "FRU Data Isn't Valid" + RESET_STYLE_BLACK_BG)
        print(RESET_STYLE)
        exit()
    # get data len in hex from the data that we read
    data_len_hex_msb = str(hex(fru_data[9]))[2:]  # get the hex number
    data_len_hex_lsb = str(hex(fru_data[10]))[2:]  # get the hex number
    # if the hex number is 0x9 for example it will become 9
    if len(data_len_hex_lsb) == 1:
        data_len_hex_lsb = "0" + data_len_hex_lsb
    if len(data_len_hex_msb) == 1:
        data_len_hex_msb = "0" + data_len_hex_msb
    # convert data len to decimal
    data_len = 0
    data_len += HEX_TO_DECIMAL[data_len_hex_lsb[1]]  # first byte
    data_len += HEX_TO_DECIMAL[data_len_hex_lsb[0]] * 16  # second byte
    data_len += HEX_TO_DECIMAL[data_len_hex_msb[1]] * 16 * 16  # third byte
    data_len += HEX_TO_DECIMAL[data_len_hex_msb[0]] * 16 * 16 * 16  # fourth byte
    # check if fru_data really contains data_len + 11
    if not len(fru_data) >= data_len + 11:
        print(RED_COLOR + "FRU Data Isn't Valid" + RESET_STYLE_BLACK_BG)
        print(RESET_STYLE)
        exit()
    # save the part of the fru that actually has data
    fru_data = fru_data[:data_len + 11]
    fru_data_byte_array = bytearray(fru_data)  # convert the data to byte array
    # save the data to a temp file
    try:
        with open(file_name + ".bin", "wb") as file:
            file.write(fru_data_byte_array)
        output_file_name = file_name
    except OSError:
        print(RED_COLOR + "Couldn't Open '%s'" % file_name, RESET_STYLE_BLACK_BG)
        with open("output.bin", "wb") as file:
            file.write(fru_data_byte_array)
        output_file_name = "output"
        print(GREEN_COLOR + "Output Saved To 'output.bin'.")
    return output_file_name


def print_fru_file_data(var_for_out, verbose=True, file_name="onie_eeprom", read_from_fru=True):
    """
    prints the fru data from the file_name.bin file
    :param var_for_out:
    :param verbose: print everything or just return the codes and codes_data from the file
    :param file_name: the name of the file to read the data from (and possibly out put the fru data to)
    :param read_from_fru: output data from fru or read directly from a file
    :type verbose: bool
    :type file_name: str
    :type read_from_fru: bool
    :return: a tuple of 2 lists, the first list contains all the fields codes, the second list contains all the fields
             data (in the same order as the first list)
    :rtype: tuple (of 2 lists that contain str)
    """
    RUN_ON = var_for_out
    savetolog = ''
    checksum_in_fru = None
    checksum_should_be = 0
    codes = []
    codes_data = []
    tracking_number = None
    if file_name.endswith(".bin"):
        file_name = file_name[:-4]
    if read_from_fru:
        output_file_name = output_fru_data_to_bin_file(fru_adr=var_for_out, file_name=file_name, verbose=verbose)
    else:
        if os.path.isfile(file_name + ".bin"):
            output_file_name = file_name
        else:
            print(RED_COLOR + "ERROR File Doesn't Exist" + RESET_STYLE_BLACK_BG)
            print(RESET_STYLE)
            exit()
    # open the file with the fru data
    with open(output_file_name + ".bin", "rb") as file:
        data = file.read()
    if not len(data) >= 11:
        print(RED_COLOR + "FRU File Isn't Valid." + RESET_STYLE_BLACK_BG)
        print(RESET_STYLE)
        exit()
    # get ID String and check
    index = 0
    id_string = data[index:index + 8]
    index += 8
    is_id_string_ok = id_string == HEADER_STRING
    if is_id_string_ok:
        if verbose:
            savetolog += "ID String - OK \n"
    else:
        savetolog += "ID String - Not Ok \n"
        print(RESET_STYLE)
        exit()
    # get Header Version and check
    header_version = data[index:index + 1]
    index += 1
    is_header_version_ok = header_version == HEADER_VERSION
    if is_header_version_ok:
        if verbose:
            savetolog += "Header Version - OK \n"
    else:
        savetolog += "Header Version - Not Ok \n"
        print(RESET_STYLE)
        exit()
    data_len = 0
    # get data len in hex from the data that we read
    data_len_hex_msb = str(hex(data[index]))[2:]  # get the hex number
    index += 1
    data_len_hex_lsb = str(hex(data[index]))[2:]  # get the hex number
    index += 1
    # if the hex number is 0x9 for example it will become 9
    if len(data_len_hex_lsb) == 1:
        data_len_hex_lsb = "0" + data_len_hex_lsb
    if len(data_len_hex_msb) == 1:
        data_len_hex_msb = "0" + data_len_hex_msb
    # convert data len to decimal
    data_len += HEX_TO_DECIMAL[data_len_hex_lsb[1]]  # first byte
    data_len += HEX_TO_DECIMAL[data_len_hex_lsb[0]] * 16  # second byte
    data_len += HEX_TO_DECIMAL[data_len_hex_msb[1]] * 16 * 16  # third byte
    data_len += HEX_TO_DECIMAL[data_len_hex_msb[0]] * 16 * 16 * 16  # fourth byte)
    if len(data) > data_len + 11:
        checksum_should_be = binascii.crc32(data[:data_len+11-4])
    elif len(data) == data_len + 11:
        checksum_should_be = binascii.crc32(data[:-4])
    else:
        print(RED_COLOR + "Erorr Getting File Checksum." + RESET_STYLE_BLACK_BG)
        print(RESET_STYLE)
        exit()
    #if verbose:
        #savetolog += "-" * 64 + "\n"
        #savetolog += " " * 3 + "Code Meaning" + " " * 6 + "|     " + "Code" + "     |" + " " * 9 + "Data" + " " * 13 + "|" + "\n"
        #savetolog += "\n"
    while index - 8 - 1 - 2 < data_len:
        code = data[index:index + 1].hex()
        index += 1
        if code not in ALLOWED_CODES or code not in CODES_MEANING:
            print("Unknown Code '%s'." % code)
            print(RESET_STYLE)
            exit()
        code_meaning = CODES_MEANING[code]
        codes.append(code)
        if verbose:
            if code == "fd":  # if code == "fd" add row space
                savetolog += "\n"
            savetolog += code_meaning
            savetolog += " " * (21 - len(code_meaning))
            savetolog += code
            savetolog += " " * 6
            # if code == "fd":  # if code == "fd" skip data in this row as the data will be printed in multiple rows
            #     print(" " * 22 + "|\n")
        if code in ALLOWED_CODES:
            pass
        elif code in NOT_ALLOWED_CODES:
            savetolog += "EEPROM data isn't valid" + "\n"
            print(RESET_STYLE)
            exit()
        else:
            savetolog += "Unrecognized code at position %d, code =" % (index - 1), code + "\n"
            print(RESET_STYLE)
            exit()
        ok = False
        if code is None:
            pass
        elif code in ALLOWED_CODES:
            ok = True
            len_of_current_field_hex = data[index:index + 1].hex()
            index += 1
            len_of_current_field_decimal = 0
            len_of_current_field_decimal += HEX_TO_DECIMAL[len_of_current_field_hex[1]]
            len_of_current_field_decimal += HEX_TO_DECIMAL[len_of_current_field_hex[0]] * 16
        else:
            savetolog += "EEPROM data isn't valid" + "\n"
            print(RESET_STYLE)
            exit()
        if ok:
            field_data = data[index:index + len_of_current_field_decimal]
            index += len_of_current_field_decimal
            if code == "24":
                codes_data.append(field_data.hex().upper())
                if verbose:
                    savetolog += field_data.hex().upper() + " " * (22 - len(field_data.hex().upper())) + "\n"
            elif code == "2a":
                field_data = field_data.hex().upper()
                while field_data.startswith("0"):
                    field_data = field_data[1:]
                codes_data.append(field_data)
                if verbose:
                    savetolog += field_data + " " * (22 - len(field_data))
            elif code == "fd":
                codes_data.append(field_data)
                if field_data[:4].hex() != "00003d4e":
                    savetolog += "Vendor Extension IANA enterprise number is incorrect!!!!!!!!!!!!" + "\n"
                if verbose:
                    field_data = field_data[4:]
                    if RUN_ON == 1:
                        savetolog += "\n"
                        # 4 chars
                        savetolog += "Silicom Onie Version:" + " " * (31 - len("Silicom Onie Version:") - 2) + str(field_data[:4])[2:-1] + " " * (22 - len(str(field_data[:4])[2:-1])) + "\n"
                        field_data = field_data[4:]
                        savetolog += "Tracking Number:" + " " * (31 - len("Tracking Number:") - 2) + str(field_data)[2:-1] + " " * (22 - len(str(field_data)[2:-1])) + "\n"
                        tracking_number = str(field_data)[2:-1]
                    else:
                        savetolog += str(field_data)[2:-1] + " " * (22 - len(str(field_data)[2:-1])) + "\n"
            elif code == "fe":
                codes_data.append(field_data.hex().upper())
                if verbose:
                    savetolog += field_data.hex().upper() + " " * (22 - len(field_data.hex().upper())) + "\n"
                checksum_in_fru = field_data.hex().upper()
            elif code == "ff":
                break
            else:
                codes_data.append(field_data.decode())
                if verbose:
                    savetolog += field_data.decode() + " " * (22 - len(field_data.decode())) + "\n"
            if code in ["fd", "fe"]:
                if verbose:
                    savetolog += "\n"
    if checksum_in_fru == hex(checksum_should_be)[2:].upper():
        is_checksum_correct = "Checksum is ok"
    else:
        is_checksum_correct = "Checksum is incorrect !!!!!!!!!!!!!!!!!!"
    if verbose:
        #savetolog += "-" * 64 + "\n"
        if "ok" not in is_checksum_correct:
            savetolog += "Checksum should be %s\n" % hex(checksum_should_be)[2:].upper() + "%s" % is_checksum_correct + "\n"
        else:
            savetolog += "Checksum should be %s\n" % hex(checksum_should_be)[2:].upper() + "%s" % is_checksum_correct + "\n"
    # backup fru file
    if not os.path.isdir("Backup_FRU_Files"):
        os.makedirs("Backup_FRU_Files")
    if tracking_number is not None:
        shutil.copy(file_name + ".bin", "Backup_FRU_Files/" + tracking_number + ".bin")
    return codes, codes_data, savetolog


def main(RUN_ON, tracknum):
    print(RESET_STYLE_BLACK_BG, end="")
    import_packages_that_are_not_included_in_python()
    linux_check_if_package_installed_and_install_if_not("i2c-tools")
    print()
    p = subprocess.Popen("i2cdetect -l".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    if RUN_ON == 1:
        expected_vendor = "Silicom"
        expected_product_name = "Lisbon2"
        expected_part_number = "P3IMB1-M-P1"
        expected_label_revision = "1.70"
        expected_manufacturer = "Silicom"
        expected_country_code = "IL"
    elif RUN_ON == 2: #if new card / fru, add another elif
        expected_vendor = "Silicom"
        expected_product_name = "Dual LBG GEN4"
        expected_part_number = "PE416IS2LBLL"
        expected_label_revision = "1.20"
        expected_manufacturer = "Silicom"
        expected_country_code = "IL"
    expected_tracking_number = tracknum #input("Please Enter The Card Tracking Number: ")
    while len(expected_tracking_number) != 13:
        print("Tracking Is Wrong.")
        expected_tracking_number = input("Please Enter The Card Tracking Number: ")
    get_i2c_bus_number_and_enable_access()
    codes, codes_data, savetolog = print_fru_file_data(var_for_out=RUN_ON)
    pass_fail = True
    if codes_data[codes.index("2d")] != expected_vendor:
        savetolog += "Expected Vendor:" + expected_vendor
        savetolog += "Vendor In FRU:  " + codes_data[codes.index("2d")]
        pass_fail = False
    if codes_data[codes.index("21")] != expected_product_name:
        savetolog += "Expected Product Name:" + expected_product_name
        savetolog += "Product Name In FRU:  " + codes_data[codes.index("21")]
        pass_fail = False
    if codes_data[codes.index("22")] != expected_part_number:
        savetolog += "Expected Part Number:" + expected_part_number
        savetolog += "Part Number In FRU:  " + codes_data[codes.index("22")]
        pass_fail = False
    if codes_data[codes.index("27")] != expected_label_revision:
        savetolog += "Expected Label Revision:" + expected_label_revision
        savetolog += "Label Revision In FRU:  " + codes_data[codes.index("27")]
        pass_fail = False
    if codes_data[codes.index("2b")] != expected_manufacturer:
        savetolog += "Expected Manufacturer:" + expected_manufacturer
        savetolog += "Manufacturer In FRU:  " + codes_data[codes.index("2b")]
        pass_fail = False
    if codes_data[codes.index("2c")] != expected_country_code:
        savetolog += "Expected Country Code:" + expected_country_code
        savetolog += "Country Code In FRU:  " + codes_data[codes.index("2c")]
        pass_fail = False
    if str(codes_data[codes.index("fd")])[-14:-1] != expected_tracking_number:
        savetolog += "Expected Tracking Number:" + expected_tracking_number
        savetolog += "Tracking Number In FRU:  " + str(codes_data[codes.index("fd")])[-14:-1]
        pass_fail = False
    if pass_fail:
        #print(GREEN_COLOR + "-" * 64 + RESET_STYLE_BLACK_BG)
        #print(GREEN_COLOR + "FT Passed" + RESET_STYLE_BLACK_BG)
        #print(GREEN_COLOR + "-" * 64 + RESET_STYLE_BLACK_BG)
        print("PASS FRU")
    else:
        print(RED_COLOR + "-" * 64 + RESET_STYLE_BLACK_BG)
        print(RED_COLOR + "FT Failed" + RESET_STYLE_BLACK_BG)
        print(RED_COLOR + "-" * 64 + RESET_STYLE_BLACK_BG)
    if os.path.isfile("onie_eeprom.bin"):
        os.remove("onie_eeprom.bin")
    return savetolog


if __name__ == '__main__':
    main()