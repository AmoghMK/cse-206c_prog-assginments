import collections
import time

# From https://www.asciitable.com/
ASCII_FREQ = {
    32: 0.1874,
    69: 0.096,
    84: 0.0702,
    65: 0.0621,
    79: 0.0584,
    73: 0.0522,
    78: 0.0521,
    72: 0.0487,
    83: 0.0477,
    82: 0.0443,
    68: 0.0352,
    76: 0.032,
    85: 0.0225,
    77: 0.0194,
    67: 0.0188,
    87: 0.0182,
    71: 0.0166,
    70: 0.0162,
    89: 0.0156,
    80: 0.0131,
    44: 0.0124,
    46: 0.0121,
    66: 0.0119,
    75: 0.0074,
    86: 0.0071,
    34: 0.0067,
    39: 0.0044,
    45: 0.0026,
    63: 0.0012,
    88: 0.0012,
    74: 0.0012,
    59: 0.0008,
    33: 0.0008,
    81: 0.0007,
    90: 0.0007,
    58: 0.0003,
    49: 0.0002,
    48: 0.0001,
    40: 0.0001,
    41: 0.0001,
    42: 0.0001
}

for i in range(65,91):
    ASCII_FREQ[i+32] = ASCII_FREQ[i]*0.9
    ASCII_FREQ[i] = ASCII_FREQ[i]*0.1

with open("cipher.txt", "r") as f:
    cipher = f.read()

cipher = "".join([chr(int(cipher[i:i+2],16)) for i in range(0, len(cipher), 2)])
# print(cipher)
# time.sleep(2)

max_sum = 0
max_sum_key_length = 0

for key_length in range(1,51):
    sum = 0
    for j in range(key_length):
        subsum = 0
        l = []
        start = j
        while start<len(cipher):
            l.append(cipher[start])
            start+=key_length
        n = len(l)
        l = collections.Counter(l)
        for val in l.values():
            freq = (val/n)
            subsum += freq**2
        sum += subsum/key_length
    if sum>max_sum:
        max_sum = sum
        max_sum_key_length = key_length
    print(key_length, sum)

print()
print(max_sum)
print(max_sum_key_length)


final_key = []
for sub in range(max_sum_key_length):
    subset = []
    start = sub
    while start < len(cipher):
        subset.append(cipher[start])
        start += key_length
    n = len(subset)
    subset = collections.Counter(subset)
    max_freq = 0
    max_freq_shift = None
    for shift in range(256):
        flag = True
        freq_sum = 0
        for key, val in subset.items():
            if (ord(key)^shift)>128:
                flag = False
                break
            freq_sum += (val/n) * ASCII_FREQ.get((ord(key)^shift), 0)
        if flag and freq_sum > max_freq:
            max_freq = freq_sum
            max_freq_shift = shift
    print(sub, max_freq)
    final_key.append(max_freq_shift)

print()
print(final_key)
print("".join(chr(x) for x in final_key))

out = ""
for i in range(len(cipher)):
    out += chr(ord(cipher[i]) ^ final_key[i%max_sum_key_length])
print()
time.sleep(2)
print(out)
