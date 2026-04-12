import math
def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, y = egcd(e, phi)
    if gcd != 1:
        return None
    return x % phi

p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))
n = p * q
phi = (p - 1) * (q - 1)
e = int(input("Enter public exponent e (gcd(e, phi) = 1): "))
d = mod_inverse(e, phi)
if d is None:
    print("Modular inverse does not exist. Choose a different e.")
    exit()
print("\nPublic Key (e, n):", (e, n))
print("Private Key (d, n):", (d, n))
m = int(input("\nEnter message (number) to encrypt: "))
c = pow(m, e, n)
print("Encrypted message:", c)
m_decrypted = pow(c, d, n)
print("Decrypted message:", m_decrypted)