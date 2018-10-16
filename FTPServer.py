#AUTHOR: VICTOR YEO
#PID: 730250927
#Homework 5 - Server Program

import sys
import shutil
import os.path
import re
import socket

#global variables
lastKnownHost = ""
lastKnownPort = ""

def checkInput(cmd):
	isUser = 0 #to check whether username has alr been given
	isLoggedIn = 0 #to check whether signed in
	index = 0 #to record commands entered
	retrCalled = 0 #to record whether retr has been called
	portCalled = 0#to record whether PORT called
	hasQuit = 0#to record whether quit was called
	socketEstablished = False

	#create welcoming socket first
	
	portNumber = int(cmd) #extracting the port number to be used

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip = socket.gethostbyname(socket.gethostname())
	address = (ip,portNumber)
	server_socket.bind(address)
	server_socket.listen(1) #Allow only one connection at a time

	connection_socket,addr = server_socket.accept()	
	sys.stdout.write("220 COMP 431 FTP server ready.\r\n")
	connection_socket.send(("220 COMP 431 FTP server ready.\r\n").encode())
	hasSent = 1	
	socketEstablished = True

	while socketEstablished:
		receivedFile = connection_socket.recv(1024).decode()		
		sentences = receivedFile.splitlines(keepends = True)

		for sentence in sentences:
				
			sys.stdout.write(sentence)
			sentence = sentence.lstrip()
			cmd = sentence.split()
			firstChar = cmd[0].upper()

			if (hasQuit == 1):
				connection_socket.close()
				quit()
				socketEstablished = False
				break		

			if (firstChar != "USER" and  firstChar != "PASS" and firstChar != "TYPE" and firstChar != "SYST" and firstChar != "NOOP" and firstChar != "QUIT" and firstChar != "PORT" and firstChar != "RETR"):
				sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
				connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
				continue
			#first case
			elif (firstChar == "USER"):
				numWhitespace = 0 #number of white spaces in the sentence

				for char in sentence[5:-2]:
					if ord(char) > 127: #check through all characters to ensure they are ASCII characters
						sys.stdout.write("501 Syntax error in paramter.\r\n")
						connection_socket.send(("501 Syntax error in parameter\r\n").encode())
						continue

					elif char == " ":
						numWhitespace += 1

				if (len(sentence) == 5 or len(sentence) == 6):
					sys.stdout.write("501 Syntax error in parameter.\r\n") #when the input string is a command error, and not a username error (noted in the HW1 pdf
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				elif sentence[4] != " ": 
					sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
					continue

				elif numWhitespace == len(sentence[5:-2]):
					sys.stdout.write ("501 Syntax error in parameter.\r\n") #to capture empty username
					connection_socket.send(("501 Syntax error in parameter\r\n").encode())
					continue

			
				elif (sentence[-2:] != "\r\n" ):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue
		
				else:
					sys.stdout.write ("331 Guest access OK, send password.\r\n")
					connection_socket.send(("331 Guest access OK, send password.\r\n").encode())
					isUser = 1
					continue

			#second case
			elif (firstChar == "PASS"):	
				numWhitespace = 0 #number of white spaces in the sentence

				for char in sentence[5:-2]:
					if ord(char) > 127: #check through all characters to make sure they are ASCII characters
						sys.stdout.write("501 Syntax error in parameter.\r\n")
						connection_socket.send(("501 Syntax error in parameter\r\n").encode())
						continue

					elif char == " ":
						numWhitespace += 1
				
				if (isUser == 0):
					sys.stdout.write("503 Bad sequence of commands.\r\n")
					connection_socket.send(("503 Bad sequence of commands.\r\n").encode())
					continue

				elif numWhitespace == len(sentence[5:-2]): #to capture empty password
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter\r\n").encode())
					continue

				elif sentence[4] != " ":
					sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
		
				elif (len(sentence) == 5 or len(sentence) == 6):
					sys.stdout.write ("500 Syntax error, command unrecognized.\r\n") #when the input string is a command error, and not a passcode error (noted in the HW1 pdf
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())		
					continue

				elif (sentence[-2:] != "\r\n" ):
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				else: 
					sys.stdout.write("230 Guest login OK.\r\n")
					connection_socket.send(("230 Guest login OK.\r\n").encode())
					isLoggedIn = 1
					continue

			#third case	
			elif (firstChar == "TYPE"):
			
				if (isLoggedIn == 0):
					sys.stdout.write("530 Not logged in.\r\n")
					connection_socket.send(("530 Not logged in.\r\n").encode())
					continue

				elif (len(sentence) == 5 or len(sentence) == 6):
					sys.stdout.write("500 Syntax error, command unrecognized.\r\n") #when the input string is a command error, and not a typecode error (noted in the HW1 pdf
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
					continue

				elif(sentence[5] != "A" and sentence[5] != "I"):
					sys.stdout.write("501 Syntax error in parameter\r\n")
					connection_socket.send(("501 Syntax error in parameter\r\n").encode())
					continue

				elif (sentence[-2:] != "\r\n" ):
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				else: 
					typeCode = sentence[4:]
					typeCode = typeCode.lstrip()
					typeCode = typeCode[:-2]
					sys.stdout.write("200 Type set to " + typeCode + ".\r\n")
					connection_socket.send(("200 Type set to " + typeCode + ".\r\n").encode())
					continue

			#fourth case
			elif (firstChar == "NOOP"):
				if (isLoggedIn == 0):
					sys.stdout.write ("530 Not logged in\r\n")
					connection_socket.send(("530 Not logged in\r\n").encode())
					continue

				if (sentence[-2:] != "\r\n" ):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue
		
				elif (len(sentence) > 6):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				elif (isLoggedIn == 0):
					sys.stdout.write ("530 Not logged in.\r\n")
					connection_socket.send(("530 Not logged in.\r\n").encode())
					continue
		
				else:
					sys.stdout.write ("200 Command OK.\r\n")
					connection_socket.send(("200 Command OK.\r\n").encode())
					continue

			#fifth case
			elif (firstChar == "SYST"):
				if (isLoggedIn == 0):
					sys.stdout.write("530 Not logged in.\r\n")
					connection_socket.send(("530 Not logged in.\r\n").encode())
					continue

				if (sentence[-2:] != "\r\n" ):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				elif (len(sentence) > 6):
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				else:
					sys.stdout.write("215 UNIX Type: L8.\r\n")
					connection_socket.send(("215 UNIX Type: L8.\r\n").encode())
					continue

			#6th case
			elif (firstChar == "QUIT"):
				if (sentence[-2:] != "\r\n" ):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue
				elif (len(sentence) > 6):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue
				else:
					sys.stdout.write ("221 Goodbye.\r\n")
					connection_socket.send(("221 Goodbye.\r\n").encode())
					connection_socket.close()
					socketEstablished = False
					quit() #to reinitialise all internal values
					break

			#7th case
			elif (firstChar == "PORT"):

				if (isLoggedIn == 0):
					sys.stdout.write("530 Not logged in.\r\n")
					connection_socket.send(("530 Not logged in.\r\n").encode())
					continue

				elif (len(sentence) == 5 or len(sentence) == 6):
					sys.stdout.write ("500 Syntax error, command unrecognized.\r\n") #when the input string is a command error, and not a typecode error (noted in the HW1 pdf
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
					continue

				elif(len(portList) != 6):
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				elif (sentence[-2:] != '\r\n'):
					sys.stdout.write ("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				else:
					portCalled = 1
					hostPort = sentence[4:-2].strip()
					portList = hostPort.split(',')
					hostAddress = portList[0:4]
					portNumber = portList[4:6]

					for number in portList:
						if int(number) > 255 or int(number) < 0:
							sys.stdout.write("501 Syntax error in parameter.\r\n")
							connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
							continue

				#translate host-port to ipport
					translatedChar = int(portList[-2]) * 256 + int(portList[-1])
					actualAddress = portList[0]+'.'+portList[1]+'.'+portList[2]+'.'+portList[3]+','+str(translatedChar)

					lastKnownHost = portList[0]+'.'+portList[1]+'.'+portList[2]+'.'+portList[3]
					lastKnownPort = str(translatedChar)
					sys.stdout.write("200 Port command successful (" + actualAddress +").\r\n")
					connection_socket.send(("200 Port command successful (" + actualAddress +").\r\n").encode())
					continue

			#8th case
			elif (firstChar == "RETR"):
				
				hasBeenCalled = retrCalled
			
				if (isLoggedIn == 0):
					sys.stdout.write("501 Syntax error in parameter\r\n")			
					connection_socket.send(("501 Syntax error in parameter\r\n").encode())
					continue

				elif (portCalled != 1 or retrCalled == 1):
					sys.stdout.write("503 Bad sequence of commands.\r\n")
					connection_socket.send(("503 Bad sequence of commands.\r\n").encode())
					continue
		
				for char in sentence[5:-2]:
					if ord(char) > 127:
						sys.stdout.write("501 Syntax error in parameter.\r\n") 
						connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
						continue

				if (len(sentence) == 5 or len(sentence) == 6):
					sys.stdout.write ("500 Syntax error, command unrecognized.\r\n") #when the input string is a command error, and not a typecode error (noted in the HW1 pdf
					connection_socket.send(("500 Syntax error, command unrecognized.\r\n").encode())
					continue

				elif (sentence[-2:] != '\r\n'):
					sys.stdout.write("501 Syntax error in parameter.\r\n")
					connection_socket.send(("501 Syntax error in parameter.\r\n").encode())
					continue

				else:
					source = sentence[4:-2].strip()
					retrCalled = 1
					
					try :
				#when file status is determined to be okay
						os.path.isfile(source)	
						sys.stdout.write("150 File status okay.\r\n")
						connection_socket.send(("150 File status okay.\r\n").encode())

					except FileNotFoundError:
						sys.stdout.write("550 File not found or access denied.\r\n")
						connection_socket.send(("550 File not found or access denied.\r\n").encode())
						continue
					
					#need to try creating a connection; if cannot, reply
					fileSocketMain = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					clientIp = socket.gethostbyname(socket.gethostname())

					try:	
						fileSocketMain.connect(clientIp, int(lastKnownPort))
	
					except Exception:
						connection_socket.send(("425 Can not open data connection.\r\n").encode())
						continue

					with open(source,'rb') as f:
						l = f.read(1024)
						while(l):
							fileSocketMain.send(l)
							l = f.read(1024)
					f.close()

					sys.stdout.write("250 Requested file action completed.\r\n")
					connection_socket.send(("250 Requested file action completed.\r\n").encode())	
					fileSocketMain.close()
					portCalled = 0
					continue

					
			
						

def quit():
	isUser = 0 #to check whether username has alr been given
	isLoggedIn = 0 #to check whether signed in
	index = 0 #to record commands entered
	retrCalled = 0 #to record whether retr has been called
	portCalled = 0#to record whether PORT called
	hasQuit = 0#to record whether quit was called


cmd = sys.argv[1]
checkInput(cmd)

