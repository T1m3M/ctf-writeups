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
> **Hey! My friend sent me a message... He said encrypted it with the key ANGSTROMCTF.
> He mumbled what cipher he used, but I think I have a clue.
> Gotta go though, I have history homework!!
> agqr{yue_stdcgciup_padas}**

> *Hint: Keyed caesar, does that even exist??*

### solution:

Well, as it's obvious from the title it has something to do with "Ceaser Cipher" and as the hint says "Keyed Ceaser" so i used this [site](http://rumkin.com/tools/cipher/caesar-keyed.php) to decrypt the flag given the key provided and BOOM! we got the flag!

```
actf{yum_delicious_salad}
```
---

## No Canary
