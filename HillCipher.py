import numpy as np

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    return ''.join([chr(num % 26 + ord('A')) for num in numbers])

def process_text(text):
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'  # padding
    return text

def encrypt(text, key_matrix):
    text = process_text(text)
    result = ""

    for i in range(0, len(text), 2):
        pair = text[i:i+2]
        vector = np.array(text_to_numbers(pair)).reshape(2, 1)
        encrypted_vector = np.dot(key_matrix, vector) % 26
        result += numbers_to_text(encrypted_vector.flatten())

    return result

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def decrypt(cipher_text, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix)))
    det_mod = det % 26
    det_inv = mod_inverse(det_mod, 26)

    if det_inv is None:
        raise ValueError("Key matrix is not invertible")

    adjugate = np.array([[key_matrix[1][1], -key_matrix[0][1]],
                         [-key_matrix[1][0], key_matrix[0][0]]])

    inverse_matrix = (det_inv * adjugate) % 26

    result = ""

    for i in range(0, len(cipher_text), 2):
        pair = cipher_text[i:i+2]
        vector = np.array(text_to_numbers(pair)).reshape(2, 1)
        decrypted_vector = np.dot(inverse_matrix, vector) % 26
        result += numbers_to_text(decrypted_vector.flatten())

    return result


key_matrix = np.array([[3, 3],
                       [2, 5]])

plain_text = input("Enter plain text: ")

encrypted = encrypt(plain_text, key_matrix)
print("Encrypted text:", encrypted)

decrypted = decrypt(encrypted, key_matrix)
print("Decrypted text:", decrypted)