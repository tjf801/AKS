from math import floor, ceil, sqrt, gcd, log2
from decimal import *

def TestPerfectPower(n):
	for i in range(2, ceil(log2(n))+1): 
		root = n ** (1/Decimal(i))
		if round(root)==root: return True
	return False

def get_r(n):
	
	l = log2(n)
	
	maxk = floor(l ** 2)
	maxr = max(3, ceil(l ** 5))
	
	nextR = True
	
	r = Decimal(2)
	
	#for (r=2; nextR and r < maxr; r++;):
	while (nextR and (r < maxr)):
		nextR = False
		
		k = Decimal(1)
		
		#for (k = 1; (not nextR and k <= maxk); k++;):
		while (not nextR and k <= maxk):
			nextR = (pow(n, k, r) in [0, 1])
			
			k = k + 1
		
		r = r + 1
	
	r -= 1
	return r

def gcd(a, b):
	while 1:
		if a >= b:
			a = a % b
		elif a < b:
			b = b % a
		
		if a==0:
			return b
		if b==0:
			return a

def φ(n):
	t = 0
	i = 1
	while i < n:
		if gcd(n, i)==1: t += 1
		i+=1
	
	return t

def AKS_prime_check(n):
	
	if n%2 == 0: return False
	
	if TestPerfectPower(n): return False
	
	r = get_r(n)
	
	a = r
	while a > 1 and a < n:
		if gcd(a, n) != 1:
			return False
		a -= 1
	
	if n <= 5690034 and n <= r: return True
	
	a = 1
	
	bound = floor(sqrt(φ(r)) * log2(n))
		
	while a <= bound:
		if pow(a, n, n) - a != 0:
			return False
		a+=1
	
	return True
