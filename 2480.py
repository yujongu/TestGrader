"""
Test Case 1
3 3 6
Expected Result
1300

Test Case 2
2 2 2
Expected Result
12000

Test Case 3
6 2 5
Expected Result
600

Test Case 4
6 3 3
Expected Result
1300

Test Case 5
2 6 2
Expected Result
1200

"""

a, b, c = map(int, input().split())

if a == b == c:
    print(10000 + a * 1000)
elif a == b:
    print(1000 + a * 100)
elif a == c:
    print(1000 + a * 100)
elif b == c:
    print(1000 + b * 100)
else:
    print(100 * max(a, b, c))
