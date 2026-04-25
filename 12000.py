"""
Test Case 1
3
5 9
1 4
3 7
Expected Result
7

Test Case 2

Expected Result


Test Case 3

Expected Result


Test Case 4

Expected Result


Test Case 5

Expected Result


"""


n = int(input())
r = [int(input()) for _ in range(n)]

min_dist = float('inf')

for k in range(n):
    total = sum(r[i] * ((i - k) % n) for i in range(n))
    min_dist = min(min_dist, total)

print(min_dist)