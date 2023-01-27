print ("task1")
from math import exp
def f(x):
    return x-exp(-x)
DELTA=10**-9
def dichotomic (l,r):
    m=(l+r)/2
    # print (m,f(m))
    if abs(f(m))<DELTA:
        return m
    if f(m)<0:
        return dichotomic (m,r)
    else:
        return dichotomic (l,m)
print ("dichotomic ",dichotomic(0,1))
def df(x):
    x1=x-DELTA
    x2=x+DELTA
    y1= f(x1)
    y2= f(x2)
    dx= x2-x1
    dy= y2-y1
    return dy/dx

def newton(x):
    while abs(f(x))>DELTA:
        x=x-f(x)/df(x)
        # print(x,f(x))
    return x
print ("newton ",newton(42))

def iterations(x):
    while abs(f(x))>DELTA and x!=float("inf"):
        x= -f(x)+x
        # print(x,f(x))
    return x
print ("iterations ",iterations(0)) 

