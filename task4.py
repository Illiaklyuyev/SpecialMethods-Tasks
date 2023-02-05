from math import sin
print ("task4")
def f(x,y):
    return sin(x+y)+(x-y)**2-1.5*x+2.5*y
X0=0
Y0=0
M=10**-3 

def symemtrypoint(x1,y1,x2,y2,x3,y3):
    k=(y3-y2)/(x3-x2)
    b=y1+1/k*x1
    xp=(-x2*k+y2-b)/(-1/k-k)
    yp=xp*k-k*x2+y2
    xs=2*xp-x1
    ys=2*yp-y1  
    return xs,ys

def simplexmeth():
    K=1/5
    x1=X0-1*K
    y1=Y0-1*K
    x2=X0+1*K
    y2=Y0+0*K
    x3=X0+0*K
    y3=Y0+1*K
    xc_prev=1000
    yc_prev=1000
    while abs((x1+x2+x3)/3-xc_prev) >= M or abs((y1+y2+y3)/3-yc_prev) >= M:
        f1=f(x1,y1)
        f2=f(x2,y2)
        f3=f(x3,y3)
        xc_prev=(x1+x2+x3)/3
        yc_prev=(y1+y2+y3)/3
        if f1>=f2 and f1>=f3:
            xs,ys=symemtrypoint(x1,y1,x2,y2,x3,y3)
            fs=f(xs,ys)
            if fs<f1:
                x1,y1=xs,ys
            else:
                x23,y23=(x2+x3)/2,(y2+y3)/2
                x1,y1=(x23+x1)/2,(y23+y1)/2
        elif f2>=f1 and f2>=f3:
            xs,ys=symemtrypoint(x2,y2,x1,y1,x3,y3)
            fs=f(xs,ys)
            if fs<f2:
                x2,y2=xs,ys
            else:
                x13,y13=(x1+x3)/2,(y1+y3)/2
                x2,y2=(x13+x2)/2,(y13+y2)/2
        elif f3>=f2 and f3>=f1:
            xs,ys=symemtrypoint(x3,y3,x2,y2,x1,y1)
            fs=f(xs,ys)
            if fs<f3:
                x3,y3=xs,ys
            else:
                x12,y12=(x1+x2)/2,(y1+y2)/2
                x3,y3=(x12+x3)/2,(y12+y3)/2
    return (x1+x2+x3)/3,(y1+y2+y3)/3
print(simplexmeth())



    







        








