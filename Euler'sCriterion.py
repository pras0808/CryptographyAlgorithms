# Function to check if solution exists using Euler's Criterion
def has_solution(a, p):
    # Compute a^((p-1)//2) % p efficiently
    result = pow(a, (p - 1) // 2, p)
    
    if result == 1:
        return "YES"
    else:
        return "NO"


# Reading input
t = int(input().strip())

for _ in range(t):
    a, p = map(int, input().split())
    print(has_solution(a, p))