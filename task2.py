print("task2")
from random import uniform as random_float
coefs=[0,5,2,3,1]
# coefs=[-4,0,1]
def calc_polynom(coefs,x):
    sum=0
    for i in range (len(coefs)):
        c=coefs[i]
        sum=sum+c*x**i
    return sum
DELTA=10**-6
random_float
def dcalc_polynom(coefs,x):
    x1=x-(random_float(-1,1)+random_float(-1,1)*1j)/10**3
    x2=x+(random_float(-1,1)+random_float(-1,1)*1j)/10**3
    y1= calc_polynom(coefs,x1)
    y2= calc_polynom(coefs,x2)
    dx= x2-x1
    dy= y2-y1
    return dy/dx
def newton(coefs,x):
    while abs(calc_polynom(coefs,x))>DELTA:
        x=x-calc_polynom(coefs,x)/dcalc_polynom(coefs,x)
        # print(x,calc_polynom(coefs,x))
    return x
# print ("newton ",newton(coefs,42))
#print(calc_polynom(coefs,1j))
def division(coefs,a):
    coefs_=coefs[::-1]
    result=[]
    result.append(coefs_[0])
    for i in range(1,len(coefs_)-1):
        result.append(coefs_[i]+a*result[i-1])
    return result[::-1] 
# print (division(coefs,newton(coefs,42)))
while len(coefs)>1:
    sol=newton(coefs,42)
    print("sol= ",sol)
    coefs=division(coefs,sol)
    # print ("coefs= ",coefs)












