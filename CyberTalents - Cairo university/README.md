# CyberTalents - Cairo University CTF 2019

It was the first year for CyberTalents's Cybersecurity CTF Competition at Cairo University and was also my first time to participate in a real-life CTF!

**NOTE:** the descriptions of the challenges aren't accurate because they're not available after the competition has ended.


## Challenges

| Title                              | Category                        | Score |
| ---------------------------------- |:-------------------------------:| -----:|
|    [repeat](#repeat)               |   Forensics                     | 100   |
|    [ezez keygen 2](#ezez-keygen-2) |   Malware reverse engineering   | 100   |
|    [Holmes Traces](#holmes-traces) |   Forensics                     | 100   |

<hr />

## repeat
#### Forensics (100 points)

### Description
In this challenge we're given a [repeat.zip](repeat.zip) file


### solution

i checked the file by **file** command to see if zip is the true extension of it:
```
$ file repeat.zip
repeat.zip: Zip archive data, at least v2.0 to extract
```

well, it seems that .zip is the true extension!
let's unzip it!!
```
$ unzip repeat.zip
```

now we have a file called **flag** and by checking it using **file** command again: 
```
$ file flag
flag: Zip archive data, at least v2.0 to extract
```

we see that it's a zip file too! now we should rename it to **flag.zip**:
```
$ mv flag flag.zip
```

and then unzip it:
```
$ unzip flag.zip
```

i got a file called **flag** again! .. after repeating the process of renaming and unzipping the fiile again i got the same result, *so it sounds like this file is archived multiple times, right?*

and since we repeat the renaming and the unzipping process we can write a bash script to do this task for us by a for loop:
```
$ for i in {0..100}; do mv flag flag.zip && unzip flag.zip; done
```

after the script finished, now we can see a **flag.txt** which contains the flag
```
flag{Scrip7ing_is_s0_4w3som3}
```


<hr />

## ezez keygen 2
#### Malware reverse engineering (100 points)

### Description
[ezez_keygen2](ezez_keygen2) is an executable file and the task is to **crack it**


### solution
**Solved after the competition**

First, i used **gdb** to see the structure of the program:

```
$ gdb ezez_keygen2
(gdb) set disassembly-flavor intel
(gdb) disas main
```

and the output was:
```
   0x0000000000400abb <+0>:	push   rbp
   0x0000000000400abc <+1>:	mov    rbp,rsp
   0x0000000000400abf <+4>:	sub    rsp,0x20
   0x0000000000400ac3 <+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x0000000000400ac6 <+11>:	mov    QWORD PTR [rbp-0x20],rsi
   0x0000000000400aca <+15>:	cmp    DWORD PTR [rbp-0x14],0x2
   0x0000000000400ace <+19>:	jg     0x400ae4 <main+41>
   0x0000000000400ad0 <+21>:	mov    edi,0x400c20
   0x0000000000400ad5 <+26>:	call   0x4005e0 <puts@plt>
   0x0000000000400ada <+31>:	mov    eax,0xffffffff
   0x0000000000400adf <+36>:	jmp    0x400b70 <main+181>
   0x0000000000400ae4 <+41>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000000000400ae8 <+45>:	add    rax,0x8
   0x0000000000400aec <+49>:	mov    rax,QWORD PTR [rax]
   0x0000000000400aef <+52>:	mov    rdi,rax
   0x0000000000400af2 <+55>:	call   0x400670 <strdup@plt>
   0x0000000000400af7 <+60>:	mov    QWORD PTR [rbp-0x10],rax
   0x0000000000400afb <+64>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000000000400aff <+68>:	add    rax,0x10
   0x0000000000400b03 <+72>:	mov    rax,QWORD PTR [rax]
   0x0000000000400b06 <+75>:	mov    rdi,rax
   0x0000000000400b09 <+78>:	call   0x400670 <strdup@plt>
   0x0000000000400b0e <+83>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000000000400b12 <+87>:	mov    rdx,QWORD PTR [rbp-0x8]
   0x0000000000400b16 <+91>:	mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000400b1a <+95>:	mov    rsi,rdx
   0x0000000000400b1d <+98>:	mov    rdi,rax
   0x0000000000400b20 <+101>:	call   0x400a32 <check>
   0x0000000000400b25 <+106>:	cmp    eax,0x1
   0x0000000000400b28 <+109>:	jne    0x400b5c <main+161>
   0x0000000000400b2a <+111>:	mov    rax,QWORD PTR [rbp-0x10]
   0x0000000000400b2e <+115>:	mov    esi,0x400c46
   0x0000000000400b33 <+120>:	mov    rdi,rax
   0x0000000000400b36 <+123>:	call   0x400640 <strcmp@plt>
   0x0000000000400b3b <+128>:	test   eax,eax
   0x0000000000400b3d <+130>:	jne    0x400b5c <main+161>
   0x0000000000400b3f <+132>:	mov    rax,QWORD PTR [rbp-0x8]
   0x0000000000400b43 <+136>:	mov    rsi,rax
   0x0000000000400b46 <+139>:	mov    edi,0x400c55
   0x0000000000400b4b <+144>:	mov    eax,0x0
   0x0000000000400b50 <+149>:	call   0x400620 <printf@plt>
   0x0000000000400b55 <+154>:	mov    eax,0x0
   0x0000000000400b5a <+159>:	jmp    0x400b70 <main+181>
   0x0000000000400b5c <+161>:	mov    edi,0x400c68
   0x0000000000400b61 <+166>:	call   0x4005e0 <puts@plt>
   0x0000000000400b66 <+171>:	mov    edi,0xffffffff
   0x0000000000400b6b <+176>:	call   0x400660 <exit@plt>
   0x0000000000400b70 <+181>:	leave  
   0x0000000000400b71 <+182>:	ret    

```

well, at address 0x0000000000400b20 there is a function called **check** and that sounds interesting!
and by disassembling it:

``` 
(gdb) disas check

   0x0000000000400a32 <+0>:	push   rbp
   0x0000000000400a33 <+1>:	mov    rbp,rsp
   0x0000000000400a36 <+4>:	sub    rsp,0x20
   0x0000000000400a3a <+8>:	mov    QWORD PTR [rbp-0x18],rdi
   0x0000000000400a3e <+12>:	mov    QWORD PTR [rbp-0x20],rsi
   0x0000000000400a42 <+16>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000400a46 <+20>:	mov    rdi,rax
   0x0000000000400a49 <+23>:	call   0x4005f0 <strlen@plt>
   0x0000000000400a4e <+28>:	mov    QWORD PTR [rbp-0x10],rax
   0x0000000000400a52 <+32>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000000000400a56 <+36>:	mov    rdi,rax
   0x0000000000400a59 <+39>:	call   0x4005f0 <strlen@plt>
   0x0000000000400a5e <+44>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000000000400a62 <+48>:	cmp    QWORD PTR [rbp-0x10],0x1e
   0x0000000000400a67 <+53>:	ja     0x400a70 <check+62>
   0x0000000000400a69 <+55>:	cmp    QWORD PTR [rbp-0x8],0x3c
   0x0000000000400a6e <+60>:	jbe    0x400a77 <check+69>
   0x0000000000400a70 <+62>:	mov    eax,0xffffffff
   0x0000000000400a75 <+67>:	jmp    0x400ab9 <check+135>
   0x0000000000400a77 <+69>:	mov    rax,QWORD PTR [rbp-0x8]
   0x0000000000400a7b <+73>:	shr    rax,1
   0x0000000000400a7e <+76>:	cmp    rax,QWORD PTR [rbp-0x10]
   0x0000000000400a82 <+80>:	je     0x400a8b <check+89>
   0x0000000000400a84 <+82>:	mov    eax,0xffffffff
   0x0000000000400a89 <+87>:	jmp    0x400ab9 <check+135>
   0x0000000000400a8b <+89>:	mov    rax,QWORD PTR [rbp-0x20]
   0x0000000000400a8f <+93>:	mov    rdi,rax
   0x0000000000400a92 <+96>:	call   0x4008a5 <getuser>
   0x0000000000400a97 <+101>:	mov    rdx,rax
   0x0000000000400a9a <+104>:	mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000400a9e <+108>:	mov    rsi,rax
   0x0000000000400aa1 <+111>:	mov    rdi,rdx
   0x0000000000400aa4 <+114>:	call   0x400640 <strcmp@plt>
   0x0000000000400aa9 <+119>:	test   eax,eax
   0x0000000000400aab <+121>:	je     0x400ab4 <check+130>
   0x0000000000400aad <+123>:	mov    eax,0xffffffff
   0x0000000000400ab2 <+128>:	jmp    0x400ab9 <check+135>
   0x0000000000400ab4 <+130>:	mov    eax,0x1
   0x0000000000400ab9 <+135>:	leave  
   0x0000000000400aba <+136>:	ret    
```
it seems that this function do multiple tests to check for username and password and if everything is okay it follows to the address 0x0000000000400a92 to call **getuser** function

and again after we disassemble getuser function we will see **getBin** and **getIndex** functions are being called.

So the general look at this code is that the check function makes a general checks for inputs and getuser function checks if the password is correct for the current user with some mathematics by getBin and getIndex functions.

I moved then to [Ghidra](https://ghidra-sre.org/) to decompile those functions for better and detalied understanding.

i decompiled the main and i got this:
```c
undefined8 main(int param_1,long param_2)

{
  int iVar1;
  char *__s1;
  char *pcVar2;
  
  if (param_1 < 3) {
    puts("usage: ./ezez_keygen2 username serial");
    return 0xffffffff;
  }
  __s1 = strdup(*(char **)(param_2 + 8));
  pcVar2 = strdup(*(char **)(param_2 + 0x10));
  iVar1 = check(__s1,pcVar2,pcVar2);

  if ((iVar1 == 1) && (iVar1 = strcmp(__s1,"4dminUser31337"), iVar1 == 0)) {
    printf("flag is: flag{%s}\n",pcVar2);
    return 0;
  }

  puts("unrecognized user");
  exit(-1);
}
```
So to get the flag the check(username, password) must be true and the username must be "**4dminUser31337**".
*well, we got the username .. now let's go get the password!*

I decompiled check function to see what's happening there:
```c
undefined8 check(char *param_1,char *param_2)

{
  int iVar1;
  size_t sVar2;
  size_t sVar3;
  undefined8 uVar4;
  char *__s1;
  
  sVar2 = strlen(param_1);
  sVar3 = strlen(param_2);

  if ((sVar2 < 0x1f) && (sVar3 < 0x3d)) {

    if (sVar3 >> 1 == sVar2) {
      __s1 = (char *)getuser(param_2);
      iVar1 = strcmp(__s1,param_1);

      if (iVar1 == 0) {
        uVar4 = 1;
      }
      else {
        uVar4 = 0xffffffff;
      }
    }
    else {
      uVar4 = 0xffffffff;
    }
  }
  else {
    uVar4 = 0xffffffff;
  }
  return uVar4;
}
```
Now we know that:
* username must be < 30 characters
* password must be < 60 characters
* the password length should be twice the username length
* the password is passed to getuser function and it returns a string
* the string returned by getuser function should be identical to the username we entered

So the getuser function generates a string based on the password, i then studied how it's doing that and i came up with this python code which is equivalent of getuser function:

```python
LTable = "AFECWQPXIGJTUBN%"
HTable = "cpqowuejfnvhzbx$" 

# enter the password to be encrypted
password = ''
password = input("Password = ")

p = ''
counter = 0

# loop for password length
while(True):

    pass_len = len(password)
    if(pass_len <= counter):
        break
    
    # find the index of the password even-indexed letter in LTable
    even_index = LTable.find(password[counter])

    # find the index of the password odd-indexed letter in HTable
    odd_index  = HTable.find(password[counter + 1])

    # convert the index value to binary
    s = format(even_index, '04b')
    t = format(odd_index, '04b')

    # concatenate even-indexed value in binary with odd-indexed value in binary to get 1 byte
    # (e.g. [s = 0110, t = 0001] => p = 00101001)
    for x in range (0, 4):
        p += s[x]
        p += t[x]

    # seperate each byte with a space
    p += ' '
    
    # reset
    s = ''
    t = ''

    counter += 2

list_bin = p.split(' ')
list_bin.pop()

h = ""

for i in list_bin:
    # convert each byte to hex
    h = hex(int(i, 2))[2:]

    # convert each byte in hex to decimal
    h2i = int(h, 16)

    # get the ascii character
    print(chr(h2i), end = '')

print('')
```
**NOTE:** *the even-indexed characters in the input string must be in LTable and the odd-indexed characters must be in HTable*

Shortly, it iterates for each charachter in the password string and searches for it in LTable *if the character index is even* and searches for it in HTable *if the character index is odd* and then converts each value to binary (4-bits) and combine them into 1-byte (8-bits) and then gets the ascii value of this byte.

As explained this will result in a string with a half-length of password and this string must be the same as the username which we got before "**4dminUser31337**".

Now given "**4dminUser31337**" we need to reverse this encryption process to get the password!

i wrote a python code again to do this task for us which is the reverse process of the previous code:
```python
# given information
LTable = "AFECWQPXIGJTUBN%"
HTable = "cpqowuejfnvhzbx$"

# the username we need to decrypt
user = "4dminUser31337"

# username in binary
s = "00" + bin(int.from_bytes(user.encode(), 'big'))[2:]

p = ""
q = ""
flag = ""

# loop for each byte in s
for i in range(0, len(s) // 8):
    # each byte in s
    piece = s[8 * i:8 * (i+1)]
    
    # seperate the byte so even-indexed bits stored in p and odd-indexed bits stored in q
    for j in range(0, 8):
        if(j%2 == 0):
            p += piece[j]
        else:
            q += piece[j]

    # convert p and q to decimal
    LTable_index = int(p, 2)
    HTable_index = int(q, 2)

    # get the p-th letter in LTable and the q-th letter in HTable
    flag += LTable[LTable_index] + HTable[HTable_index]
    
    # reset
    p = ""
    q = ""

print(flag)
```

This will print out **WeWvPhPnXvA$QbWhQzQuWuQuQuQj** and by running the program:
```
$ ./ezez_keygen2 4dminUser31337 WeWvPhPnXvA$QbWhQzQuWuQuQuQj
unrecognized user
```

It doesn't work, why?!!
Because **$** character in bash is reserved and what comes after it is a variable name
to solve this problem we can use **\\** to escape this character

and by running the program again:
```
$ ./ezez_keygen2 4dminUser31337 WeWvPhPnXvA\$QbWhQzQuWuQuQuQj
flag is: flag{WeWvPhPnXvA$QbWhQzQuWuQuQuQj}
```

that's it!! we got the flag!
```
flag{WeWvPhPnXvA$QbWhQzQuWuQuQuQj}
```
<hr />

## Holmes Traces
#### Malware reverse engineering (100 points)

### Description
given [holmes.pcap](holmes.pcap) file .. get the flag


### solution
**Solved after the competition**

Using wireshark and after studying the capture i make an assumption about what's going on ..

there's a file **safe.tar.gz.gpg** has been sent so now we need to collect the packets and see what will happen next:
we choose a packet of the many packets of this file over FTP-DATA protocol then ``` right-click > Follow > TCP Stream ```

there's a window popup contains the stream of the file and we will choose ``` show data and save as: Raw ``` then ``` Save as > safe.tar.gz.gpg ``` 

Now we got the file notice that gpg file needs a password to be decrypted so our next step will be getting that password!

There are interesting base64 texts while we are scrolling in the pcap file .. and they all are sent over the protocol HTTP
and the source is: ``` 192.168.56.1 ``` and the destination is: ``` 192.168.56.101 ``` so our filter is:
```
http && ip.src == 192.168.56.1 && ip.dst == 192.168.56.101
```
and by decoding each base64 password:
```
QWxtb3N0VGhlcmVKdXN0cGFzcw==  ->    AlmostThereJustpass
cVNGVXFaV3pNWG5CckJTY3E=	   ->	   qSFUqZWzMXnBrBScq
MjAwQ29kZW1lYW5zPw==		      ->	   200Codemeans?
QXV0b3NweVdhdHNvbg==		      ->	   AutospyWatson
QXV0b3NweUhvbG1lcw==		      ->	   AutospyHolmes
QyJdXyt1ajxfLmZLUWs9U1k=	   ->	   C"]_+uj<_.fKQk=SY
aFNZdldEc0NrVWVySFlOdXE=	   ->	   hSYvWDsCkUerHYNuq
SEZzTU13Q1BZTkhSU3BEcGo=	   ->	   HFsMMwCPYNHRSpDpj
NWJIV3B6MmFmN3RUUHpWNVI=	   ->	   5bHWpz2af7tTPzV5R
SG9sbWVzJldhdHNvblBhc3M=	   ->	   Holmes&WatsonPass
Q2Fpcm9TZWN1cml0eUNhbXA=	   ->	   CairoSecurityCamp
U2hlcmxva0hvbG1lczI=		      ->	   SherlokHolmes2
UGFzczJyZFNvbHZlMjI=		      ->	   Pass2rdSolve22
Qy8tdHQ6KytIa2tCVWhkZyQ=	   ->	   C/-tt:++HkkBUhdg$
Yzs3WnFqTkBSbi1bZiRZJA==	   ->	   c;7ZqjN@Rn-[f$Y$
JiFzbndCQEdtWVR+a1Y5XTYl	   ->	   &!snwB@GmYT~kV9]6%
```

And by applying each password to decrypt the gpg file using this command:
```
$ gpg -d --batch --passphrase="THE PASSWORD GOES HERE" safe.tar.gz.gpg
```
we will see that 5bHWpz2af7tTPzV5R is the real password! there's ascii data floating around so now we need to improve our command:
```
$ gpg -d --batch --passphrase="5bHWpz2af7tTPzV5R" safe.tar.gz.gpg > safe.tar.gz
```
Now we need to decrypt the resulting file safe.tar.gz:
```
$ gunzip safe.tar.gz
$ tar -xvf safe.tar
Steg.png
```

Well, now we have a photo named Steg.png so we will conclude that the flag is hidden inside using a **Steg**anography method .. i tried many tools but [https://github.com/DimitarPetrov/stegify](stegify) did the job *make sure to install golang before*

Finally:
```
$ stegify decode --carrier Steg.png --result flag
```
The result is a JPEG photo when we open it we find this text **"N3twRk_Tr@c_hV_m@ny_Det@ls"**

```
flag{N3twRk_Tr@c_hV_m@ny_Det@ls}
```
