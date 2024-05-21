This is just a repository where my python projects are going to sit in.

In order to properly host or receive, you must change the inbound settings in 'windows defender firewall with advanced security'(ran as administrator) and ensure:
1. all python.exe and similar files are enable.
2. all file and printer sharing(Echo) type rules are enabled and active as well. 


All connecting users and the host must have the same subnet mask (use ipconfig in cmd prompt) AKA: be in the same local network
All connecting users must be connecting to the host's IPV4 address in the local network.
All connecting users and the host must have the same value for the port.
