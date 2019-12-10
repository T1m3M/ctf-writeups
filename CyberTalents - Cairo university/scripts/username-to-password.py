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
