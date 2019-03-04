#!/usr/bin/python
# This script creates the Removal config for a host/subnet to be uploaded to espresso CR

from os import walk
import sys, csv
import fileinput
import re

print ("Please enter the host IP to be removed")
host_ip = raw_input()
ConfigFile = open('Config.txt', 'w')
Template_Config = 'Checking'
no_object = []

def collect_header_delta(filename, ASA_dict):
	f = open(filename, 'r')
	header_present = 0
	no_sys = 1
	header_list = ['NA','NA','NA','NA','NA','NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA']
	header_list[0] = filename
	ingress_list = []
	egress_list = []
	global_list = []
	for line in f.readlines():
	    if "ON:" in line:
	    	header_present = 1
	        device_line = line.strip()
	        header_list[1] = device_line
	    if "OS:" in line:
	        header_present = 1
	        type_line = line.strip()
	        header_list[2] = type_line
	    if (("Begin" in line) and ("Standard Ingress" not in line) and ("Ingress" in line)):
	    	header_list[7] = line.strip()
	    elif (("!" in line) and ("OUTBOUND" not in line) and ("INBOUND" in line)):
	    	header_list[7] = line.strip()
	    if ((("ingress" in line) or ("in" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line)):
	    	ingress_line = line.strip()
	    	ingress_list.append(ingress_line)
	    if (("Begin" in line) and ("Standard Egress" not in line) and ("Egress" in line)):
	    	header_list[9] = line.strip()
	    if ((("egress" in line) or ("out" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line)):
	    	egress_line = line.strip()
	    	egress_list.append(egress_line)
	    if ((("global" in line) or ("GLOBAL" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line)):
	    	global_line = line.strip()
	    	global_list.append(global_line)
	f.close()
	if ((header_present == 1) and (no_sys == 1)):
		if (str(header_list[2]) == "!! OS: ASA"):
			data = str(ASA_dict.get(str(header_list[1])))
			for i in ingress_list:
				data += str("no " + str(i.split(',')) + "\n")
			for j in egress_list:
				data += str("no " + str(j.split(',')) + "\n")
			for k in global_list:
				data += str("no " + str(k.split(',')) + "\n")
			ASA_dict[str(header_list[1])] = data
	return ASA_dict	

def collect_Implementer_Note(filename):
	f = open(filename, 'r')
	header_present = 0
	no_sys = 1
	header_list = ['NA','NA','NA','NA']
	header_list[0] = filename
	ingress_list = []
	egress_list = []
	for line in f.readlines():
	    if "ON:" in line:
	    	header_present = 1
	        device_line = line.strip()
	        header_list[1] = device_line
	    if "OS:" in line:
	        header_present = 1
	        type_line = line.strip()
	        header_list[2] = type_line
	    if "SCP:" in line:
	    	header_present = 1
	    	command_line = line.strip()
	    	header_list[3] = command_line
	f.close()
	if ((header_present == 1) and (no_sys == 1)):
		if (str(header_list[2]) != "!! OS: ASA"):
			ConfigFile.write(str(header_list[1]) + "\n" )
			ConfigFile.write(header_list[3] + "\n\n" )

def collect_header_mystic(filename):
	""" collects Acls header data from the files """
	f = open(filename, 'r')
	header_present = 0
	no_sys = 1
	header_list = ['NA','NA','NA','NA','NA','NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA']
	header_list[0] = filename
	ingress_list = []
	egress_list = []
	global_list = []
	for line in f.readlines():
	    if "ON:" in line:
	    	header_present = 1
	        device_line = line.strip()
	        header_list[1] = device_line
	    if "PUSH:" in line:
		header_present = 1
	        push_line = line.strip()
	        header_list[2] = push_line
	    if "OS:" in line:
	        header_present = 1
	        type_line = line.strip()
	        header_list[3] = type_line
	    if "SCP:" in line:
	    	header_present = 1
	    	command_line = line.strip()
	    	header_list[4] = command_line
	    if "NETWORKS:" in line:
	    	header_present = 1
	    	command_line = line.strip()
	    	header_list[5] = command_line
	    if "CONTACT:" in line:
	    	header_present = 1
	    	bz_line = line.strip()
	    	header_list[6] = bz_line
	    if (("Begin" in line) and ("Standard Ingress" not in line) and ("Ingress" in line)):
	    	header_list[7] = line.strip()
	    elif (("!" in line) and ("OUTBOUND" not in line) and ("This is for INBOUND" in line)):
	    	header_list[7] = line.strip()
	    if ((("ingress" in line) or ("in" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line) and ("out" not in line)):
	    	ingress_line = line.strip()
	    	ingress_list.append(ingress_line)
	    elif (re.match('(.+) '  +host_ip+  ' (.+)', line) and ("egress" not in line) and ("out" not in line) and ("GLOBAL" not in line)):
	    	ingress_line = line.strip()
	    	ingress_list.append(ingress_line)
	    elif (re.match('(.+) '  +host_ip+  '/(.+)', line) and ("egress" not in line) and ("out" not in line) and ("GLOBAL" not in line)):
	    	ingress_line = line.strip()
	    	ingress_list.append(ingress_line)
	    if (("Begin" in line) and ("Standard Egress" not in line) and ("Egress" in line)):
	    	header_list[9] = line.strip()
	    elif (("!" in line) and ("INBOUND" not in line) and ("This is for OUTBOUND" in line)):
	    	header_list[9] = line.strip()
	    if ((("egress" in line) or ("out" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line) and ("in" not in line)):
	    	egress_line = line.strip()
	    	egress_list.append(egress_line)
	    if (("deny ip any any" in line) and ("GLOBAL" in line)):
	    	header_list[10] = line.strip()
	    if ((("global" in line) or ("GLOBAL" in line)) and re.match('(.+) '  +host_ip+  ' (.+)', line)):
	    	global_line = line.strip()
	    	global_list.append(global_line)
	f.close()
	if ((header_present == 1) and (no_sys == 1)):
		if (str(header_list[3]) == "!! OS: ASA"):
			for i in range(1,6):
				ConfigFile.write(header_list[i] + '\n')
			if len(ingress_list) == 0 :
				ConfigFile.write("")
			else:
				ConfigFile.write("\nUNDER:\n" + str(header_list[7]) + "\n\n")
				ConfigFile.write("REMOVE: \n")
			for i in ingress_list:
			    ConfigFile.write( str(i.split(',')) + "\n" )
			if len(egress_list) == 0:
				ConfigFile.write("")
			else:
				ConfigFile.write("\nUNDER:\n" + str(header_list[9]) + "\n\n")
				ConfigFile.write("REMOVE: \n")
			for j in egress_list:
			    ConfigFile.write( str(j.split(',')) + "\n" )
			if len(global_list) == 0:
				ConfigFile.write("")
			else:
				ConfigFile.write("\nABOVE:\n" + str(header_list[10]) + "\n\n")
				ConfigFile.write("REMOVE: \n")
			for k in global_list:
			    ConfigFile.write( str(k.split(',')) + "\n" )
			ConfigFile.write("---------------------------------------------------------------------------------------------------\n" )
		if (str(header_list[3]) != "!! OS: ASA"):
			for i in range(1,6):
				ConfigFile.write(header_list[i] + '\n')
			if len(ingress_list) == 0 :
				ConfigFile.write("")
			else:
				ConfigFile.write("\n\nREMOVE: \n")
			for i in ingress_list:
			    ConfigFile.write( str(i.split(',')) + "\n" )
			ConfigFile.write("---------------------------------------------------------------------------------------------------\n" )
	if no_sys == 0:
		global no_object
		no_object.append(filename)
def FileCheck(fn):
	""" Check if the file can be opened"""
    	try:
      		open(fn, "r")
      		return 1
    	except IOError:
      		print "Error: File does not appear to exist."
      		return 0
def Grab_Template(fn):
	""" Grab the template config to be updated in all the router acls files """
	t = open(fn, "r")
	global Template_Config
	Template_Config = t.read()
	t.close()
mypath = "/Users/pranaybomma/Desktop/Scripts/Removal/"
file_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    file_list.extend(filenames)
    break
print Template_Config
ConfigFile.write("\nDELTA-CONFIG:\n")
ConfigFile.write("#####################################\n")
ASA_dict = {}
for x in file_list:
	if (("acls." in x) and (".py" not in x)):
		print "Looking in to file " + x
	        result = FileCheck(x)
		if result == 1:
			ASA_dict = collect_header_delta(x, ASA_dict)
for key,val in ASA_dict.items():
	ConfigFile.write(key+ "\n\n" + "conf t\n")
	ConfigFile.write(val)
	ConfigFile.write( "end\n" + "copy run start" + "\n-----------------------------------------------------------------\n")		
ConfigFile.write("\n\nImplementers Dashboard\n")
ConfigFile.write("#####################################\n")
for x in file_list:
	if (("acls." in x) and (".py" not in x)):
	        result = FileCheck(x)
		if result == 1:
			collect_Implementer_Note(x)
ConfigFile.write("===================================================================================================\n")
ConfigFile.write("\n\nMYSTIC(Files to be updated):\n")
ConfigFile.write("#####################################\n")
for x in file_list:
	if (("acls." in x) and (".py" not in x)):
	        result = FileCheck(x)
		if result == 1:
			collect_header_mystic(x)
for i in no_object:
	print i
ConfigFile.close()
#to replace the '] and '[ ]
with open('Config.txt', 'r+') as infile:
    data = infile.read()
    data = data.replace("['", "")
    data = data.replace("']", "")
    data = data.replace("None", "")
    infile.truncate(0)
    infile.seek(0)
    infile.write(data)
