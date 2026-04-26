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

numbers = [int(input()) for _ in range(7)]
numbers = [num for num in numbers if num % 2 == 1]
if numbers:
    print(sum(numbers))
    print(min(numbers))
else:
    print(-1)