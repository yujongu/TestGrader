"""
Test Case 1

Expected Result


Test Case 2

Expected Result


Test Case 3

Expected Result


Test Case 4

Expected Result


Test Case 5

Expected Result


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