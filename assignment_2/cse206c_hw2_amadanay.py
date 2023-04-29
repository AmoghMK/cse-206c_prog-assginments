import collections

# From https://millikeys.sourceforge.net/freqanalysis.html
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

# Didn't find specific frequencies for uppercase and lowercase letters. 
# So, modifying english alphabet frequencies to get upper and lowercase frequencies.
# for an alphabet, x with frequency, f, I am setting the lower and upper case frequency of x as 0.9f and 0.1f respectively.
for i in range(65,91):
    ASCII_FREQ[i+32] = ASCII_FREQ[i]*0.9
    ASCII_FREQ[i] = ASCII_FREQ[i]*0.1

# reading the cipher text
with open("cipher.txt", "r") as f:
    cipher = f.read()

# converting hex encoded cipher to string of ascii characters for ease of access and use.
cipher = "".join([chr(int(cipher[i:i+2],16)) for i in range(0, len(cipher), 2)])


# FINDING KEY LENGTH

# variable to track max freq sum (E (qi)^2) and the key length we get it for. 
max_e_qi2 = 0
max_e_qi2_key_length = 0

# iterating to key_lengths of 1 to 20.
for key_length_iter in range(1,20):
    e_qi2 = 0
    # iterating for stream which is encrypted by the same key character.
    for stream_iter in range(key_length_iter):
        e_qi2_sub = 0
        stream = []
        start = stream_iter
        while start<len(cipher):
            stream.append(cipher[start])
            start+=key_length_iter
        n = len(stream)
        stream = collections.Counter(stream)
        for val in stream.values():
            freq = (val/n)
            e_qi2_sub += freq**2
        e_qi2 += e_qi2_sub/key_length_iter
    if e_qi2>max_e_qi2:
        max_e_qi2 = e_qi2
        max_e_qi2_key_length = key_length_iter


#FINDING KEY

# list to hold figured out key characters
final_key = []

# iterating for stream which is encrypted by the same key character.
for stream_iter in range(max_e_qi2_key_length):
    stream = []
    start = stream_iter
    while start < len(cipher):
        stream.append(cipher[start])
        start += max_e_qi2_key_length
    n = len(stream)
    stream = collections.Counter(stream)

    # variable to track max freq sum (E pi*(q_i+j)) and the key character we get it for. 
    max_e_pi_qij = 0
    max_e_pi_qij_key_char = None

    # Iterating through all possible key character (0-255).
    for possible_key_char in range(256):
        flag = True
        e_pi_qij = 0
        for key, val in stream.items():
            # if the character obtained after XORing cipher with possible_key_char is invalid (i.e ASCII value > 128), 
            # ignore the possible_key_char as invalid and move on to the next one.
            if (ord(key)^possible_key_char)>128:
                flag = False
                break
            e_pi_qij += (val/n) * ASCII_FREQ.get((ord(key)^possible_key_char), 0)
        if flag and e_pi_qij > max_e_pi_qij:
            max_e_pi_qij = e_pi_qij
            max_e_pi_qij_key_char = possible_key_char

    # add the key character providing max freq sum to the final key list.
    final_key.append(max_e_pi_qij_key_char)

print(final_key, '\n')

# use the key obtained to decrypt the ciphertext and get the plaintext.
decrypted_plaintext = ""
for i in range(len(cipher)):
    decrypted_plaintext += chr(ord(cipher[i]) ^ final_key[i%max_e_qi2_key_length])
print(decrypted_plaintext)
