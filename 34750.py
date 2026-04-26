"""
Test Case 1
200000
Expected Result
20000 180000

Test Case 2
800000
Expected Result
120000 680000

Test Case 3
50000
Expected Result
2500 47500

Test Case 4
60000
Expected Result
3000 57000

Test Case 5
70000
Expected Result
3500 66500

"""
n = int(input())

if n >= 1_000_000:
    rate = 0.2
elif n >= 500_000:
    rate = 0.15
elif n >= 100_000:
    rate = 0.1
else:
    rate = 0.05

give = int(n * rate)
keep = int(n * (1 - rate))

print(give, keep)