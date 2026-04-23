SBOX = [
99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,
202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,
183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,
4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,
9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,
83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,
208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,
81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,
205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,
96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,
224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,
231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,
186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,
112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,
225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,
140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22
]

RCON = [1,2,4,8,16,32,64,128,27,54]

def xor_bytes(a, b):
    return bytes(i ^ j for i, j in zip(a, b))

def sub_bytes(s):
    return bytes(SBOX[b] for b in s)

def shift_rows(s):
    return bytes([
        s[0], s[5], s[10], s[15],
        s[4], s[9], s[14], s[3],
        s[8], s[13], s[2], s[7],
        s[12], s[1], s[6], s[11]
    ])

def key_expansion(key):
    key = list(key)
    expanded = key[:]
    for i in range(10):
        temp = expanded[-4:]
        temp = temp[1:] + temp[:1]
        temp = [SBOX[b] for b in temp]
        temp[0] ^= RCON[i]
        for j in range(4):
            temp[j] ^= expanded[-16 + j]
        expanded += temp
    return expanded

def aes_encrypt_block(block, key):
    state = list(block)
    expanded = key_expansion(key)

    state = xor_bytes(state, expanded[:16])
    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = xor_bytes(state, expanded[16*r:16*(r+1)])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = xor_bytes(state, expanded[160:176])

    return bytes(state)


BLOCK_SIZE = 16
Rb = 0x87

def left_shift(block):
    shifted = int.from_bytes(block, 'big') << 1
    shifted &= (1 << 128) - 1
    return shifted.to_bytes(16, 'big')

def generate_subkeys(key):
    zero = bytes(16)
    L = aes_encrypt_block(zero, key)

    K1 = left_shift(L)
    if L[0] & 0x80:
        K1 = xor_bytes(K1, b'\x00'*15 + bytes([Rb]))

    K2 = left_shift(K1)
    if K1[0] & 0x80:
        K2 = xor_bytes(K2, b'\x00'*15 + bytes([Rb]))

    return K1, K2

def pad(block):
    pad_len = BLOCK_SIZE - len(block)
    return block + b'\x80' + b'\x00'*(pad_len-1)

def cmac(message, key):
    K1, K2 = generate_subkeys(key)

    blocks = [message[i:i+16] for i in range(0, len(message), 16)]
    if len(blocks[-1]) == 16:
        last = xor_bytes(blocks[-1], K1)
    else:
        last = xor_bytes(pad(blocks[-1]), K2)

    X = bytes(16)

    for b in blocks[:-1]:
        X = aes_encrypt_block(xor_bytes(X, b), key)

    T = aes_encrypt_block(xor_bytes(X, last), key)
    return T

msg = input("Enter message: ").encode()
key_input = input("Enter 16-char key: ").encode()

if len(key_input) != 16:
    raise ValueError("Key must be 16 bytes!")

tag = cmac(msg, key_input)
print("CMAC (hex):", tag.hex())