# CyberTalents - Cairo university
It was the first year for CyberTalents's Cybersecurity CTF Competition at Cairo University and was also my first time to participate in a real-life CTF!

## Challenges

| Title         | Category      | Score |
| ------------- |:-------------:| -----:|
|    [repeat](#repeat) |   Forensics   |   100 |

## repeat
#### Forensics (100 points)

### Description
In this challenge we're given a [repeat.zip](repeat.zip) file which have a flag text file inside

### solution
we check the file by **file** command to see if zip is the true extension of it:
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
we get a file called **flag** again! .. after repeating the process of renaming and unzipping the fiile again we will get the same result, *so it sounds like this file is archived multiple times, right?*

and since we repeat the renaming and the unzipping process we can write a bash script to do this task for us by a for loop:
```
$ for i in {0..100}; do mv flag flag.zip && unzip flag.zip; done
```
after the script finished, now we can see a **flag.txt** which contains the flag
```
flag{Scrip7ing_is_s0_4w3som3}
```
