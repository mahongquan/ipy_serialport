# -*- coding: utf-8 -*-
import time
import cmdstr
import System
from threading  import Timer,Thread
from System.IO.Ports import *
from System import *
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
		self.m_buf=Array[Byte](range(250))
		self.m_end=0
	def open(self):	
		self.port.Open()
		self.port.DataReceived += self.serialPort_DataReceived
	def pause(self)	:
		Console.Write("Press any key to continue . . . ");
		Console.ReadKey(True);
	def serialPort_DataReceived(self,e,data):
		buf=Array[Byte]((0,))
		#Console.Write(buf.Length)
		#print(self.port.Read.Overloads)
		try:
			while(True):
				#ct=self.port.Read.Overloads[Array[Byte],int,int](buf,0,buf.Length)
				ct=self.port.Read(buf,0,buf.Length)
				if self.m_end<len(self.m_buf):
					self.m_buf[self.m_end]=buf[0]
					self.m_end+=1
		except System.TimeoutException,e:
			pass
		self.treatdata()
	def treatdata(self):
		#print("treat")
		#self.showbuf()
		(find,start,end)=self.findCmd()
		#print(find)
		while(find):
			self.oneCmd(start,end)
			#print("before:"+str(self.m_end))
			self.removeCmd(start,end)
			#print("after:"+str(self.m_end))
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
			if (start==-1 and (self.m_buf[at]==ord('+') or self.m_buf[at]==ord('-') )):
				start=at;
				if (start!=0):
					print(self.m_buf[0])
					#print(start)
			elif (start!=-1 and self.m_buf[at]==10):#
					end=at
					find=True
					break
			at+=1
		return (find,start,end)
	def showbuf(self):
		s="buf:"
		for i in range(self.m_end):
			s+=String.Format("{0:x} ",self.m_buf[i])
		print(s)
	def showbytes(self,cmd):
		s=""
		for i in range(cmd.Length):
			s+=String.Format("{0:x},",cmd[i])
		print(s)
	def showCmd(self,start,end):
		s=""
		i=start
		while(i<end+1):
			s+=String.Format("{0:x} ",self.m_buf[i])
			i+=1
		print(s)
	def oneCmd(self,start,end):
		i=start
		s=""
		while(i<end+1):
			s+=chr(self.m_buf[i])
			i+=1
		print("cmd:"+s)

class NcSerial(Satoris):
	def __init__(self):
		Satoris.__init__(self)
		self.port = SerialPort("COM3");
		self.port.BaudRate = 19200;
		self.port.DataBits = 8;
		self.port.Parity = Parity.None;
		self.port.StopBits = StopBits.One;
		self.port.DtrEnable=False;
		self.port.ReadTimeout = 50
	def findCmd(self):
		#self.showbuf()
		find=False
		start=-1
		end=-1
		at=0
		while (at<self.m_end):
			if (start==-1 and self.m_buf[at]==0xfb and at+1<self.m_end and self.m_buf[at+1]==0xfc):
				start=at;
				if (start!=0):
					print(self.m_buf[0])
					print(start)
				at+=2
			elif (start!=-1 and self.m_buf[at]==0xfd and at+1<self.m_end and self.m_buf[at+1]==0xfe):#
				end=at+1
				find=True
				break
				#at+=1
			else:
				at+=1
		return (find,start,end)	
	def oneCmd(self,start,end):
		self.showCmd(start,end)
		if self.m_buf[start+2]==0xee:#error
			print("return error")
			pass
		elif self.m_buf[start+2]==0xf0:#start
			print("tick")
		else:
			print("other")		
	def sendUnlink(self):#FB FC F0 FD FE
		buf=Array[Byte]((0xFB,0xFC,0xF0,0xFD,0xFE))
		#self.showbytes(buf)
		self.port.Write(buf,0,buf.Length)
	def start(self):
		buf=Array[Byte]((0xFB,0xFC,0xF1,0xFD,0xFE))
		self.port.Write(buf,0,buf.Length)
	def stop(self):
		self.sendUnlink()
def maintp():
	tp=Satoris()
	tp.open()
	tp.pause()
def mainncs():
	n=NcSerial()
	n.open()
	#n.sendUnlink()
	#n.pause()
	n.start()
	System.Threading.Thread.Sleep(3000)
def main():
	#maintp()
	mainncs()
