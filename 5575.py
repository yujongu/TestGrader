"""
Test Case 1
9 0 0 18 0 0
9 0 1 18 0 0
12 14 52 12 15 30
Expected Result
9 0 0
8 59 59
0 0 38

Test Case 2
7 0 0 8 0 0
8 10 10 9 20 20
10 30 30 11 40 40
Expected Result
1 0 0
1 10 10
1 10 10

Test Case 3
7 0 30 8 0 20
9 10 50 10 10 40
15 30 15 16 30 10
Expected Result
0 59 50
0 59 50
0 59 55

Test Case 4
7 30 0 8 20 0
12 40 10 13 20 15
20 50 30 21 10 35
Expected Result
0 50 0
0 40 5
0 20 5

Test Case 5
7 30 30 8 20 20
11 40 50 12 15 10
15 15 15 16 10 10
Expected Result
0 49 50
0 34 20
0 54 55

"""
for i in range(3):
    sh, sm, ss, eh, em, es = map(int, input().split())
    start = (sh*3600)+(sm*60)+ss
    end = (eh*3600)+(em*60)+es
    t = end - start
    h = t//3600
    m = (t%3600)//60
    s = (t%3600)%60
    
    print(h, m, s)