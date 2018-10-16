#AUTHOR: YEO WEI TECK VICTOR
#PID: 730250927
#LAB 3 - PROGRAMME 2
#FTP Replies parser

import sys

def ftpParser(allInput):
	
	for line in allInput:
		sys.stdout.write(line) #echo line of input
		lineArr = line.split()
		text = lineArr[1:-2]
		error = 0
		ftpReply = lineArr[0]
		getOut = 0

		for char in lineArr[0]:
			if char.isdigit() == False:
				print("ERROR -- reply-code")
				getOut = 1
				break

		if(getOut == 1):
			continue #continue with for loop

		#test 1: reply code
		if int(lineArr[0]) < 100 or int(lineArr[0]) >= 600:
			print("ERROR -- reply-code")
			continue	
	
		#test 2: reply text
		for word in text:
			for char in word:
				if ord(char) > 127:				
					print("ERROR -- reply-text")
					error = 1
					break
			if (error == 1):
				break

		if (error == 1):
			continue

		#test 3: crlf
		if (line[-2:] != '\r\n'):
			print("ERROR -- <CRLF>")
			error = 1
			continue

		if (error == 0):
			sys.stdout.write("FTP reply " + str(ftpReply) + " accepted.  Text is : " + line[4:-2] + "\n")
			continue

cmd = sys.stdin.readlines()
main(cmd)
