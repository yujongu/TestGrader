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

Expected Result


Test Case 4

Expected Result


Test Case 5

Expected Result


"""

n = int(input())
track_list = list(input().split())
pick_track = input()

print(track_list.count(pick_track))
