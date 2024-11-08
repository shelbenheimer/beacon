#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer)

import random
import platform
import sys
import subprocess
from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/shelbenheimer)"
ALPHANUMERIC = [ 'A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '4', '5', '6', '7', '8', '9' ]

class Broadcast:
	def __init__(self, ssid, bssid, interface):
		self.ssid = ssid
		self.bssid = bssid
		self.interface = interface

	def ConstructPacket(self):
		rsn_info = (
    		b"\x01\x00"         # RSN Version: 1
    		b"\x00\x0f\xac\x09" # Group Cipher Suite: AES-GCMP WPA3
    		b"\x01\x00"         # Pairwise Cipher Suite Count
    		b"\x00\x0f\xac\x09" # Pairwise Cipher Suite List: AES-GCMP
    		b"\x01\x00"         # Auth Key Management Suite Count
    		b"\x00\x0f\xac\x08" # Auth Key Management List: SAE
    		b"\x00\x00"         # RSN Capabilities
		)

		dot11 = Dot11(type=0, subtype=8, addr1="FF:FF:FF:FF:FF:FF", addr2=self.bssid, addr3=self.bssid)
		beacon = Dot11Beacon(cap="ESS+privacy")
		
		essid = Dot11Elt(ID="SSID", info=self.ssid, len=len(self.ssid))
		rates_elt = Dot11Elt(ID="Rates", info=b"\x82\x84\x8b\x96\x0c\x12\x18\x24")
		rsn_elt = Dot11Elt(ID=48, info=rsn_info)

		packet = RadioTap() / dot11 / beacon / essid / rates_elt / rsn_elt
		return packet

def RandomBSSID():
	valid = list("FF:FF:FF:FF:FF:FF")

	temporary = []
	for byte in valid:
		if not byte == ":":
			temporary.append(random.choice(ALPHANUMERIC))
			continue

		temporary.append(":")
	return "".join(temporary)

def EnableMonitoring(interface):
	print(f"Enabling monitoring mode for {interface}.")
	subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)
	subprocess.run(["sudo", "airmon-ng", "start", f"{interface}"], stdout=subprocess.DEVNULL)

def DisableMonitoring(interface):
	print(f"Disabling monitoring mode for {interface}.")
	subprocess.run(["sudo", "airmon-ng", "stop", f"{interface}"], stdout=subprocess.DEVNULL)
	subprocess.run(["sudo", "ip", "link", "set", f"{interface}", "up"], stdout=subprocess.DEVNULL)
	subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], stdout=subprocess.DEVNULL)

try:
	if not platform.system() == "Linux":
		print("This tool is exclusive to Linux.")
		sys.exit()

	print(BANNER)

	ssid = input("ssid> ")
	interface = input("interface> ")
	bssid = RandomBSSID()

	EnableMonitoring(interface)
	
	broadcast = Broadcast(ssid, bssid, interface)
	packet = broadcast.ConstructPacket()
	sendp(packet, inter=0.1, loop=1, verbose=False, iface=broadcast.interface)

	DisableMonitoring(interface)

except Exception as error:
	print(error)