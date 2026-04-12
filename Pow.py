class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x = 1 / x
            n = -n

        result = 1.0

        while n > 0:
            # If n is odd, multiply result
            if n % 2 == 1:
                result *= x

            # Square the base
            x *= x
            n //= 2

        return result