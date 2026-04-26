"""
Test Case 1
260000
4
20000 5
30000 2
10000 6
5000 8
Expected Result
Yes

Test Case 2
250000
4
20000 5
30000 2
10000 6
5000 8
Expected Result
No

Test Case 3
5000
1
5000 1
Expected Result
Yes

Test Case 4
10000
2
5000 1
5000 1
Expected Result
Yes

Test Case 5
15000
3
5000 1
5000 1
5000 1
Expected Result
Yes

"""
x = int(input())
n = int(input())
sum = 0
for i in range(n):
  price, cnt = map(int, input().split())
  sum += (price*cnt)

if x == sum:
  print("Yes")
else:
  print("No")