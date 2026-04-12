def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result


def decrypt(cipher_text, shift):
    return encrypt(cipher_text, -shift)



plain_text = input("Enter plain text: ")
shift = int(input("Enter shift value: "))

encrypted = encrypt(plain_text, shift)
print("Encrypted text:", encrypted)

decrypted = decrypt(encrypted, shift)
print("Decrypted text:", decrypted)