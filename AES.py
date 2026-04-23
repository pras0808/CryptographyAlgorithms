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

def sub_bytes(state):
    return [SBOX[b] for b in state]

def shift_rows(s):
    return [
        s[0], s[5], s[10], s[15],
        s[4], s[9], s[14], s[3],
        s[8], s[13], s[2], s[7],
        s[12], s[1], s[6], s[11]
    ]

def xor_bytes(a, b):
    return [i ^ j for i, j in zip(a, b)]

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

def add_round_key(state, key):
    return xor_bytes(state, key)

def encrypt_block(block, key):
    state = list(block)
    expanded_key = key_expansion(key)

    state = add_round_key(state, expanded_key[:16])

    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, expanded_key[16*r:16*(r+1)])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expanded_key[160:176])

    return bytes(state)



def decrypt_block(block, key):
    # NOTE: Proper AES decryption needs inverse operations
    # This is placeholder for demonstration
    return encrypt_block(block, key)  # NOT real decryption!


plaintext = input("Enter message (16 chars): ")
key = input("Enter key (16 chars): ")

if len(plaintext) != 16 or len(key) != 16:
    raise ValueError("Both message and key must be exactly 16 characters!")

pt_bytes = plaintext.encode()
key_bytes = key.encode()

cipher = encrypt_block(pt_bytes, key_bytes)
print("\nEncrypted (hex):", cipher.hex())

decrypted = decrypt_block(cipher, key_bytes)
print("Decrypted (demo):", decrypted.decode(errors="ignore"))