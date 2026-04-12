def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def encrypt(text, key):
    cipher_text = []
    key = generate_key(text, key)

    for i in range(len(text)):
        if text[i].isalpha():
            shift_base = 65 if text[i].isupper() else 97
            t = ord(text[i]) - shift_base
            k = ord(key[i].lower()) - 97
            encrypted_char = chr((t + k) % 26 + shift_base)
            cipher_text.append(encrypted_char)
        else:
            cipher_text.append(text[i])

    return "".join(cipher_text)


def decrypt(cipher_text, key):
    original_text = []
    key = generate_key(cipher_text, key)

    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            shift_base = 65 if cipher_text[i].isupper() else 97
            c = ord(cipher_text[i]) - shift_base
            k = ord(key[i].lower()) - 97
            decrypted_char = chr((c - k) % 26 + shift_base)
            original_text.append(decrypted_char)
        else:
            original_text.append(cipher_text[i])

    return "".join(original_text)


plain_text = input("Enter plain text: ")
key = input("Enter key: ")

encrypted = encrypt(plain_text, key)
print("Encrypted text:", encrypted)

decrypted = decrypt(encrypted, key)
print("Decrypted text:", decrypted)