def diffie_hellman(p, g, a, b):
    A = pow(g, a, p)  # Alice sends to Bob
    B = pow(g, b, p)  # Bob sends to Alice

    key_alice = pow(B, a, p)
    key_bob = pow(A, b, p)

    return A, B, key_alice, key_bob


# Read inputs
p = int(input("Enter prime number (p): "))
g = int(input("Enter generator (g): "))
a = int(input("Enter Alice private key (a): "))
b = int(input("Enter Bob private key (b): "))

A, B, key_alice, key_bob = diffie_hellman(p, g, a, b)

print("\n--- Results ---")
print("Alice sends A:", A)
print("Bob sends B:", B)
print("Shared key computed by Alice:", key_alice)
print("Shared key computed by Bob:", key_bob)