import math
import sys
input = sys.stdin.readline

t = int(input().strip())

for _ in range(t):
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    unique = set(arr)
    
    if not unique:
        print("NO")
        continue
    
    g = 0
    for x in unique:
        g = math.gcd(g, x)
    
    if g == 1:
        print("YES")
    else:
        print("NO")