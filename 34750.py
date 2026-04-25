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