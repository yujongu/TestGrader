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

Expected Result


Test Case 3

Expected Result


Test Case 4

Expected Result


Test Case 5

Expected Result


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