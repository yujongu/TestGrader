"""
Test Case 1
5
4
7
8
6
4
Expected Result
48

Test Case 2
3
1
1
1
Expected Result
3

Test Case 3
3
100
1
1
Expected Result
3

Test Case 4
3
1
100
1
Expected Result
3

Test Case 5
3
1
1
100
Expected Result
3

"""


n = int(input())
r = [int(input()) for _ in range(n)]

min_dist = float('inf')

for k in range(n):
    total = sum(r[i] * ((i - k) % n) for i in range(n))
    min_dist = min(min_dist, total)

print(min_dist)