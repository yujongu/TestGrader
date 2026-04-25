"""
Test Case 1
12
77
38
41
53
92
85
Expected Result
256
41

Test Case 2
2
4
20
32
6
10
8
Expected Result
-1

"""
numbers = [int(input()) for _ in range(7)]
numbers = [num for num in numbers if num % 2 == 1]
if numbers:
    print(sum(numbers))
    print(min(numbers))
else:
    print(-1)