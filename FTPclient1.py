#AUTHOR: YEO WEI TECK VICTOR
#PID: 730250927
#LAB 5 - Client Programme

import socket
import sys
connect = "CONNECT"
get = "GET"

#global variables
isConnected = 0
hostPort = ""
pathName = ""
portNumber = 8000
commands = [connect, get]

def main(cmd):
	linArr = []
	for line in cmd:
		sys.stdout.write(line)
		lineArr = line.split(" ")
		if (line[0:4] == "QUIT"):
			quitCmd(lineArr)

		elif lineArr[0] in commands:
			lineArr[0] = lineArr[0].strip()
			if lineArr[0] ==  connect: #note that isConnect will be the last check on the input (after determining that input is valid command)
				connectCmd(lineArr)
			elif lineArr[0] == get:
				getCmd(lineArr)
		else:
			print("ERROR -- request")


def connectCmd(lineArr):

	#need to check whether its in the format CONNECT<SP>+<server_host><SP>+<server-port><EOL>
	#<Server_host> = <domain> = <element> | <element>"."<domain> 
	#<element> = <a><let-dig-str>
	#<a> = any alphabet 
	#<let-dig-str> = <let-dig> | <let-dig><let-dig-str> 
	#essentially just a string of letters and digits, starting with a letter, and either followed by '.' or not, which will then be followed by another string starting with letter

	if (serverHostCheck(lineArr[1]) and serverPortCheck(lineArr[2])):

		if(int(lineArr[2]) > 65535):
			sys.stdout.write("ERROR -- server-port\n")
			return
		global isConnected
		global hostPort
		global pathName
		global portNumber
		isConnected = 1
		sys.stdout.write("CONNECT accepted for FTP server at host " + lineArr[1] + " and port " + lineArr[2])		
		hostPort = ""
		pathName = ""
		portNumber = 8000
		
		#std output
		sys.stdout.write("USER anonymous\r\n")
		sys.stdout.write("PASS guest@\r\n")
		sys.stdout.write("SYST\r\n")
		sys.stdout.write("TYPE I\r\n")
		lineArr[1] = lineArr[1].strip()
		lineArr[2] = lineArr[2].strip()
	
	elif (serverHostCheck(lineArr[1]) == False):
		print("ERROR -- server-host")

	elif (serverPortCheck(lineArr[2]) == False):
		print("ERROR -- server-port")



def getCmd(lineArr):
	global pathName
	global portNumber
	global isConnected

	if(serverPathNameCheck(lineArr[1])):
		if (isConnected == 1):
			pathName = lineArr[1]
			sys.stdout.write("GET accepted for " + lineArr[1])
			#generate host-port = <host-address>","<port-number>
			myIp = socket.gethostbyname(socket.gethostname())
			hostArray = myIp.split('.')
				
			hostAddress = hostArray[0] + "," + hostArray[1] + "," + hostArray[2] + "," + hostArray[3]
			#to get port number, use portNumber/256 and portNumber %256 
			firstPort = int(portNumber / 256)
			secondPort = portNumber % 256
			sys.stdout.write("PORT " + hostAddress + "," +  str(firstPort) + "," + str(secondPort) + "\r\n")
			pathName = pathName.strip()
			sys.stdout.write("RETR " + pathName + "\r\n")
			portNumber+=1

		else:
			print("ERROR -- expecting CONNECT")
	#only check if is connected after validating command

	else:
		print("ERROR -- pathname")


def quitCmd(lineArr):
	global isConnected
	global pathName
	global portNumber

	#only check if it is connected after validating command
	if (isConnected == 1):
		sys.stdout.write("QUIT accepted, terminating FTP client\n")
		sys.stdout.write("QUIT\r\n")
	else:
		print("ERROR -- expecting CONNECT")

def serverHostCheck(line):
	for char in line:
		if (char.isalpha() == False  and (char != '.')):
			return False
	return True
			
def serverPortCheck(line):
	line = line[:-1]
	for char in line:
		if (char.isdigit() == False):
			return False
	if ((len(line)>1 and line[0] == 0)):
		return False

	return True

def serverPathNameCheck(line):
	for char in line:
		if (ord(char) > 127):
			return False
	return True

cmd = sys.stdin.readlines()
main(cmd)
