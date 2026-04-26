"""
Test Case 1
12
50000
Expected Result
45000

Test Case 2
23
3000
Expected Result
1000

Test Case 3
0\n100
Expected Result
100

Test Case 4
4\n50000
Expected Result
50000

Test Case 5
5\n100
Expected Result
0

"""
N = int(input())
price = int(input())
sale = [0]	# N이 5 미만일 때 처리하기 위한 0
 
if N >= 5 :
    sale.append(500)	# 500원 할인
if N >= 10 :
    sale.append(price // 10)	# 10% 할인
if N >= 15 :
    sale.append(2000)	# 2000원 할인
if N >= 20 :
    sale.append(price // 4)	# 25% 할인
 
result = price - max(sale)
if result < 0 :	# 원래 금액 - 할인 금액이 0 미만일 때
    result = 0	# 지불할 금액은 0원
print(result)