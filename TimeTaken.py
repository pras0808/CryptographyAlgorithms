class Solution:
    def secondsToRemoveOccurrences(self, s: str) -> int:
        zeros = 0
        time = 0

        for ch in s:
            if ch == '0':
                zeros += 1
            elif zeros > 0:
                time = max(time + 1, zeros)

        return time