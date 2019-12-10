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
