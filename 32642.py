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
1\n1
Expected Result
1

Test Case 4
1\n0
Expected Result
-1

Test Case 5
2\n1 1
Expected Result
3

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