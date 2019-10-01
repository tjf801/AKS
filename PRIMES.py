from math import floor, ceil, sqrt, gcd, log2, log10
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
	
	while (nextR and (r < maxr)):
		nextR = False
		
		k = Decimal(1)
		
		while (not nextR and k <= maxk):
			nextR = (pow(n, k, r) in [0, 1])
			
			k = k + 1
		
		r = r + 1
	
	r -= 1
	return r

def gcd(a, b):
	while True:
		if a >= b:
			a = a % b
		elif a < b:
			b = b % a
		
		if a==0:
			return b
		if b==0:
			return a

def gcd_extended(a,b):
	#Thanks to Robert-Campbell-256 on github for this
	a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1
	if(a < 0):
		a = -a; aneg=-1
	if(b < 0):
		b = -b; bneg=-1
	while (1):
		quot = -(a // b)
		a = a % b
		a1 = a1 + quot*a2; b1 = b1 + quot*b2
		if(a == 0):
			return (b, a2*aneg, b2*bneg)
		quot = -(b // a)
		b = b % a;
		a2 = a2 + quot*a1; b2 = b2 + quot*b1
		if(b == 0):
			return (a, a1*aneg, b1*bneg)

def modinverse(a, n):
	(gcd, ax, bn) = gcd_extended(a, n)
	if gcd!= 1: raise ValueError("Modular inverse does not exist")
	return ax % n

def lcm(a, b):
	c = a * b
	c = c / gcd(a, b)
	try: c=int(c)
	except: pass
	return c

def φ(n):
	t = 0
	i = 1
	while i < n:
		if gcd(n, i)==1: t += 1
		i+=1
	
	return t

def λ(n):
	if type(n) is list:
		#TODO: make this actually correct
		t = 1
		for i in n: t = lcm(t, (i-1))
		return t
	
	elif type(n) is int:
		if TestPerfectPower(n):
			for r in range(ceil(log2(N))+1):
				p = n ** (1/Decimal(i))
				if round(p)==p:
					return (p**(r-1)) * (p-1)
		else:
			#TODO
			pass

def isPrime(n):
	#Basic AKS Primality Check, no fancyness needed
	#runs in O(log2(n)^5)
	
	if n%2 == 0: return False
	
	if TestPerfectPower(n): return False
	
	r = get_r(n)
	
	a = r
	#for (a=r; a>1 && a<n; a--;)
	while a > 1 and a < n:
		g = gcd(a, n)
		if g != 1:
			print("factor: " + str(g))
			return False
		a -= 1
	
	if n <= 5690034 and n <= r: return True
	
	a = 1
	
	bound = floor(sqrt(φ(r)) * log2(n))
	
	#for (a=1; a<=bound; a++;)
	while a <= bound:
		if pow(a, n, n) - a != 0:
			return False
		a+=1
	
	return True


#Sieve prime check adapted from https://github.com/smanikar/primality-testing/blob/master/proposal/src/AKS.java
def sieveEratos():
	global sieveSize 
	sieveSize = 1000000
	global sieveArray 
	sieveArray = [False] * (sieveSize+1)
	sieveArray[1] = True
	i = 2
	while i < sqrt(sieveSize):
		if sieveArray[i] is not True:
			j = i * i
			while j <= sieveSize: sieveArray[j] = True; j+=i
		i+=1

def checkSievePrime(val):
	return not sieveArray[int(val)]

def largestFactor(num):
	i = int(num)
	if i==1: return i
	while i > 1:
		while sieveArray[i]:
			i-=1
		if num%i == 0:
			return i
		i-=1
	return num

def mPower(x, y, n):
	return pow(x, y, n)

def sieve_prime_check(n):
	log = floor(log10(n))
	
	sieveEratos()
	
	if TestPerfectPower(n): return False
	r = Decimal(2)
	x = r
	
	
	#for (r=2; r<n; r++;)
	while r<n:
		if gcd(r, n)!=1: print("checking r", r); return False
		
		if checkSievePrime(r):
			print("checking r", r, end="\r")
			quot = largestFactor(r - 1)
			divisor = (r - 1) / quot
			tm = 4 * (sqrt(r)) * log;
			powOf = mPower(n, divisor, r);
			if quot>=tm and powOf != 1: break
		
		r += 1
	
	print("found r of " + str(r))
	
	aLimit = ceil(2 * sqrt(r) * log)
	
	aCounter = Decimal(1)
	#for (aCounter = 1; aCounter < aLimit; aCounter++;)
	while aCounter < aLimit:
		print("checking", aCounter, end="\r")
		aBigNum = aCounter
		leftH = (mPower(x-aBigNum, n, n))%n
		rightH = (mPower(x, n, n)-aBigNum) % n
		if leftH != rightH: print("checking", aCounter); return False
		aCounter+=1
	
	print("\n")
	
	return True

def fasterfactor(n):
	i = Decimal(2)
	p = Decimal(1)
	k = n
	factors = []
	if sieve_prime_check(n): factors.append(n)
	while (p*p <= k and i*i <= k):
		if n % i == 0:
			n = n / i
			p = p * i
			factors.append(i)
			if p==k or sieve_prime_check(n): break
		else:
			i = i + 1
	if p != k:
		factors.append(int(k/p))
	
	return factors


#n = Decimal(input())
#getcontext().prec = 2*len(str(n))
#print(sieve_prime_check(n))