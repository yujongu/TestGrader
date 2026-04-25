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