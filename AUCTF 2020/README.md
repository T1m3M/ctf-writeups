# AUCTF 2020
<div align="center"><img src="AUCTF2020.png" alt="AUCTF 2020"></div>

AUCTF 2020 has ended, and me and my team [**P1rates**](https://ctftime.org/team/113157) really enjoyed it as it was full of good problems, I participated as **T1m3-m4ch1n3** and here's my writeup about some of the problems that i solved.
*(if you're interested in the rest you can read the writeup of my teammate **y4mm1** [here](https://ah-sayed.github.io/posts/auctf-2020))*

## Challenges

| Title                           	      | Category      |
| --------------------------------------------|--------------:|
| [Cracker Barrel](#cracker-barrel)	      |   Reversing   |
| [Mr. Game and Watch](#mr.-game-and-watch)   |   Reversing   |
| [Sora](#sora)      		   	      |   Reversing   |
| [Don't Break Me](#don't-break-me)	      |   Reversing   |
| [Thanksgiving Dinner](#thanksgiving-dinner) |   Pwn         |

---

## Cracker Barrel
#### Reversing

### Description:
> **I found a USB drive under the checkers board at cracker barrel. My friends told me not to plug it in but surely nothing bad is on it?<br>
> I found this file, but I can't seem to unlock it's secrets. Can you help me out?<br><br>
> Also.. once you think you've got it I think you should try to connect to challenges.auctf.com at port 30000 not sure what that means, but it written on the flash drive..<br>
> [cracker_barrel](cracker%20barrel/cracker_barrel)**

### Solution:

Firstly we start by `strings` command and obviously the flag isn't there so we do `file` command we will find it's ELF 64-bit, dynamically linked and not stripped.<br>

let's do some radare2 stuff
```
$ r2 -AA cracker_barrel
[0x00001180]> afl
```

well, here we find some interesting function names like:
```
main
sym.check
sym.check_1
sym.check_2
sym.check_3
sym.print_flag
```

then seeking to the main and entering the visual mode:
```
[0x00001180]> s main
[0x000012b5]> VV
```

we notice that main calls sym.check and then `test eax, eax` and the `je` if it's false then it calls sym.print_flag .. So whatever happens inside check() function it MUST return a non-zero value so we can get the flag!

By digging into check() function we see clearly the it takes the user input and calls check_1() function and if the return is zero it returns zero (which we don't need to happend), Otherwise it continues to call the second check which is check_2() and so on with check_3() .. so we need to make sure to return a non-zero value from these functions too

Now going deeper inside check_1():

<div align="center"><img src="assests/cracker1.png" alt="r2 screenshot"></div>

as we see clearly it takes the user input in s1 variable, then "starwars" in s2 and compares them if they're equal then it goes to the second check which compares the user input with "startrek" if they're NOT equal it returns 1

So all we need to do is passing "starwars" as first input and by that we passed the first check!

Now we go to check_2() function in visual mode we'll find there's a string "si siht egassem terces" that get modified by some operations and then compared to our second input

<div align="center"><img src="assests/cracker2.png" alt="r2 screenshot"></div>

as seen in the photo above we can make a breakpoint in the `cmp` instruction and examine the 2 strings
I'll use gdb for the debugging:
```
$ gdb cracker_barrel
(gdb) set disassembly-flavor intel
(gdb) disass check_2
   ..
   0x0000000000001553 <+132>:	mov    rsi,rdx
   0x0000000000001556 <+135>:	mov    rdi,rax
   0x0000000000001559 <+138>:	call   0x1130
   ..

(gdb) b *check_2+138
Breakpoint 1 at 0x1559

(gdb) r
Give me a key!
starwars
You have passed the first test! Now I need another key!
AAAA

Breakpoint 1, 0x0000555555555559 in check_2 ()
```

Now we hit the breakpoint on the comparing point now by examining rsi and rdi:
```
(gdb) x/wx $rsi
0x7fffffffc540:	0x41414141
(gdb) x/2wx $rdi
0x555555559420:	0x73692073	0x00000000
```

Clearly rsi is our input and rdi is how our input must be! which represents "s is" as a string (in little endian)!
And this our second input!

Now heading to our final check which is check_3 function() in visual mode .. we se a string "z!!b6~wn&\`" passed seperately to variables
then it iterates through each character in the user input string and encrypt it as follows:

<div align="center"><img src="assests/cracker1.png" alt="r2 screenshot"></div>

The encryption method:
- take each character and add 0x2 to its hexadecimal value
- XOR the result with 0x14

And then compare the n-th character in the resulting string with the n-th character in "z!!b6\~wn&\`" string.
Our goal now is clear which is to decrypt "z!!b6\~wn&\`" string:
```python
secret = "z!!b6~wn&`"
result = ""

for c in secret:
    result += chr((ord(c) ^ 0x14) - 0x2)

print(result)
```

Now by running it:
```bash
$ python3 decrypt.py
l33t hax0r
```

And that's our third input!
Now by connecting to the server to get the flag:
```
$ nc challenges.auctf.com 30000
Give me a key!
starwars
You have passed the first test! Now I need another key!
s is
Nice work! You've passes the second test, we aren't done yet!
l33t hax0r
Congrats you finished! Here is your flag!
auctf{w3lc0m3_to_R3_1021}
```

Flag: `auctf{w3lc0m3_to_R3_1021}`

---
