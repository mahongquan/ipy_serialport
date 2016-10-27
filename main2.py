# -*- coding: utf-8 -*-
import time
import cmdstr
import System
from threading  import Timer,Thread
from System.IO.Ports import *
from System import *
# m_buf=bytearray('\0' * 1024)
# m_end=0
# s = Serial()
# cmdstrs=cmdstr.getcmds()
# class MyThread(Thread):
# 	def run(self):
# 		while(True):
# 			print("hi")
# 			s.write(cmdstrs[2])
# 			time.sleep(1)
# def hello():
# 	print("send")
# 	s.write(cmdstrs[2])
# def oneCmd(cmd):
# 	for i in range(len(cmd)):
# 		print(cmd[i])
# 	if cmd[2]==0xee:#error
# 		pass
# 	elif cmd[2]==0xf1 and len(cmd)==5:#start
# 		#t = Timer(1.0, hello)
# 		#t.start()
# 		t=MyThread()
# 		t.start()
# 	elif cmd[2]==0xf0:#stop
# 		pass
# def ncsdemo():
# 	global m_buf,m_end,s
# 	s.self.port=4	#COM5
# 	s.baudrate = 19200
# 	s.bytesize = 8
# 	s.stopbits=1
# 	s.parity='N'
# 	s.open()
# 	while True:
# 		r=s.read()
# 		if m_end<len(m_buf):
# 			m_buf[m_end]=r
# 			m_end+=1
# 		treatdata()
# 		time.sleep(1)
# def getCmd(start,end):
# 	global m_buf,m_end
# 	r=bytearray('\0' * (end-start+1) )
# 	for i in range(len(r)):
# 		r[i]=m_buf[start+i]
# 	i=end+1
# 	while(i<m_end):
# 		m_buf[i-end-1]=m_buf[i]
# 		i+=1
# 	m_end=m_end-(end+1);
# 	return r
# def findCmd():
# 	find=False
# 	start=-1
# 	end=-1
# 	at=0
# 	while (at<m_end):
# 		if (m_buf[at]==0xfb and at+1<m_end and m_buf[at+1]==0xfc):#FB FC F0 FD FE
# 			start=at;
# 			if (start!=0):
# 				print(start)
# 		elif (start!=-1 and m_buf[at]==0xfd and at+1<m_end and m_buf[at+1]==0xfe):#FB FC F0 FD FE
# 				end=at+1
# 				find=True
# 		at+=1
# 	return (find,start,end)
# def testtp():
# 	global m_buf,m_end
# 	s = Serial()
# 	s.self.port=0	#COM5
# 	s.baudrate = 1200
# 	s.bytesize = 7
# 	s.stopbits=1
# 	s.parity='O'
# 	s.open()
# 	while True:
# 		r=s.read()
# 		if m_end<len(m_buf):
# 			m_buf[m_end]=r
# 			m_end+=1
# 		treatdata()
# def treatdata():
# 	(find,start,end)=findCmd()
# 	if (find):
# 		cmd=getCmd(start,end);
# 		oneCmd(cmd);
# def hello2():
#     print "hello, world"	
class Satoris:
	def __init__(self):
		self.port = SerialPort("COM1");
		self.port.BaudRate = 1200;
		self.port.DataBits = 7;
		self.port.Parity = Parity.Odd;
		self.port.StopBits = StopBits.One;
		#self.port.Handshake=Handshake.XOnXOff;
		self.port.DtrEnable=True;
		self.port.ReadTimeout = 50
		self.port.DataReceived += self.serialPort_DataReceived
		self.port.Open()
		self.m_buf=Array[Char](range(50))
		self.m_end=0
	def pause(self)	:
		Console.Write("Press any key to continue . . . ");
		Console.ReadKey(True);
	def serialPort_DataReceived(self,e,data):
		#print(e,data)
		#print("receive")
		#size = self.port.ReadBufferSize
		buf=Array[Char]({0})
		try:
			while(True):
				ct=self.port.Read(buf,0,buf.Length)
				if self.m_end<len(self.m_buf):
					self.m_buf[self.m_end]=buf[0]
					self.m_end+=1
		except System.TimeoutException,e:
			pass
		self.treatdata()
	def treatdata(self):
		#self.showbuf()
		#print("treat")
		#self.showbuf()
		(find,start,end)=self.findCmd()
		#print(find)
		while(find):
			self.oneCmd(start,end)
			print("before:"+str(self.m_end))
			self.removeCmd(start,end)
			print("after:"+str(self.m_end))
			(find,start,end)=self.findCmd()
	def removeCmd(self,start,end):
		#r=bytearray('\0' * (end-start+1) )
		# for i in range(r.Count()):
		# 	r[i]=self.m_buf[start+i]
		i=end+1
		while(i<self.m_end):
			self.m_buf[i-end-1]=self.m_buf[i]
			i+=1
		self.m_end=self.m_end-(end+1);
		#return r
	def findCmd(self):
		#self.showbuf()
		find=False
		start=-1
		end=-1
		at=0
		while (at<self.m_end):
			#print(ord(self.m_buf[at]))
			if (start==-1 and (self.m_buf[at]=='+' or self.m_buf[at]=='-')):
				start=at;
				if (start!=0):
					print(ord(self.m_buf[0]))
					#print(start)
			elif (start!=-1 and ord(self.m_buf[at])==10):#
					end=at
					find=True
					break
			at+=1
		return (find,start,end)
	def showbuf(self):
		s="buf:"
		for i in range(self.m_end):
			s+=String.Format("{0:x} ",ord(self.m_buf[i]))
		print(s)
	def showbytes(self,cmd):
		s=""
		for i in range(cmd.Length):
			s+=String.Format("{0:x},",cmd[i])
		print(s)
	def oneCmd(self,start,end):
		i=start
		s=""
		while(i<end+1):
			s+=self.m_buf[i]
			i+=1
		print("cmd:"+s)
def maintp():
	tp=Satoris()
	tp.pause()
def main():
	maintp()
