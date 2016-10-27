#import serial
def getcmds():
	f=open("FB FC F0 FD FE_2.txt").read()
	f=f.replace("\n","")
	bs=f.split(" ")
	s=""
	for b in bs:
		if b!='':
			b=r'\x'+b
			exec("a='"+b+"'")
			#print(hex(ord(a[0])))
			s+=a
	print(len(s))
	cmds=s.split('\xfb')
	truecmds=[]
	for cmd in cmds:
		if len(cmd)==0:
			pass
		else:
			truecmds.append('\xfb'+cmd)
	print(len(truecmds))
	return truecmds
