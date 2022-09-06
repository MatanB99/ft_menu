ft_menu.py by Matan Bathan.

ft_menu.py is a small and quick FT test for Silicom cards.

To use the script, there are 2 simple steps:
	1 - Choose the card to run FT on.
	2 - Enter log name (Tracking number).

The script will return 2 possible outcomes:
Option 1 - PASS
	The script will return minimal results to the user and detailed information in the log file.

Option 2 - FAIL
	The script will return detailed information on the test that has failed to the user and the log file.

Tests available as of ver 1.0:
	USB check
	MAC check
	PCI check
	FRU check

#Note - Card #1 'Pizza card' is for practice and testing the script

To add a new card to the menu:
	Define new function with the appropriate tests and params, example:
		def card_x():
			print("you chose card_x")													#prints the card chosen
			logname = str(input("Tracking: "))											#asks for the log name, usually T/N
			portnum = 8																	#amount of ports
			venid = "8086:1592"															#vendor ID of the card
			pcispeed = 8																#speed of the PCI
			pciwidth = 8																#Width of the PCI
			macadrs = str(input("mac adr: ")) 											#MAC address of the card, if it has
			with open(logname + ".txt", "a+") as f:										#creates and opens the log file
				f.write("Checked on: " + date.today().strftime("%d/%m/%Y") + "\n")		#logs the date of testing
				f.write(PCI_CHECK.checkpci(portnum, venid, pcispeed, pciwidth) + "\n")	#performs and logs the PCI test
				f.write(usb_test())														#performs and logs the USB test				
				f.write(str(MAC_CHECK.mac_compare(venid, macadrs)))						#performs and logs the MAC test
				f.write(str(FRU_CHECK.main(2, logname)))								#performs and logs the FRU test
				f.close()																#closes and saves the changes to the log file
	Add the new function to the menu() funcion:
		elif card == x:
		tracking_check()
        card_x()
				#this works as following:
				#if the entered choice in the menu equals x, gets the tracking and performs tests for card_x
		
		
To add a new test to the script:
Option 1:
	Add the test directly within the script by defining a new funcion.
Option 2:
	Import the test as a module from another python script

After that, under the "with open" statement add your test:
	f.write(NEW_TEST(params, if, needed))
#Note - don't forget to add the card number and name to the menu output text. 
