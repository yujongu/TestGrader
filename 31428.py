"""
Test Case 1
1
C
A
Expected Result
0

Test Case 2
5
I A I S S
S
Expected Result
2

Test Case 3
1\nA\nA
Expected Result
1

Test Case 4
2\nC S\nI
Expected Result
0

Test Case 5
3\nI I I\nI
Expected Result
3

"""

n = int(input())
track_list = list(input().split())
pick_track = input()

print(track_list.count(pick_track))
