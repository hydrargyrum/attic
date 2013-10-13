wakeonwan is a Ruby command-line tool for waking your machine up 
remotely. If your router is configured to route Wake-on-WAN packets, 
and your machine has WoW enabled in the BIOS, you can wake your 
machine remotely by typing:

> wakeonwan 1.2.3.4 11:22:33:44:55:66

where 1.2.3.4 is your public IP address, and 11:22:33:44:55:66 the MAC 
address of the machine to wake up.
