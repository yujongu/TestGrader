"""
Test Case 1
5
0 0 0 0 0
Expected Result
-15

Test Case 2
6
1 1 0 0 1 0
Expected Result
5

Test Case 3

Expected Result


Test Case 4

Expected Result


Test Case 5

Expected Result


"""
N = int(input())
weather = list(map(int, input().split()))
anger = [0] * N  # 각 날 마다의 분노 리스트
status = 0  # 동우의 현재 분노 0
 
for i in range(N):
    if weather[i] == 1:
        status += 1
    elif weather[i] == 0:
        status -= 1
 
    anger[i] = status
 
print(sum(anger))