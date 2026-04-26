"""
Test Case 1
2\n1000
Expected Result
20

Test Case 2
3\n1500
Expected Result
35

Test Case 3
0\n0
Expected Result
0

Test Case 4
0\n1000
Expected Result
0

Test Case 5
0\n1001
Expected Result
0

"""
N = int(input())
W = int(input())
result = N * 10
if N >= 3:
    result += 20
if N == 5:
    result += 50
if W > 1000:
    result -= 15
    
print(result if result > 0 else 0)