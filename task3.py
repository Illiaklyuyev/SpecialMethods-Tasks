from math import sqrt
print ("task3")
def f(x,y):
    return (1-x)**2 + 100*(y-x**2)**2
X_SOL=1
Y_SOL=1
X0=-2
Y0=1.5
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
    while abs((x1+x2+x3)/3-X_SOL) >= M or abs((y1+y2+y3)/3-Y_SOL) >= M:
        f1=f(x1,y1)
        f2=f(x2,y2)
        f3=f(x3,y3)
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
# print(simplexmeth())

def coordiantemeth():
    x=X0
    y=Y0
    while abs(x-X_SOL) >= M or abs(y-Y_SOL) >= M:
        xmin=x-2
        xmax=x+2
        while True:
            xml=(xmax+xmin*2)/3
            xmr=(xmax*2+xmin)/3
            if f(xml,y)>f(xmr,y):
                xmin=xml
            else:
                xmax=xmr
            if xmax-xmin<M:
                break
        x=(xmax+xmin)/2

        ymin=y-2
        ymax=y+2
        while True:
            yml=(ymax+ymin*2)/3
            ymr=(ymax*2+ymin)/3
            if f(x,yml)>f(x,ymr):
                ymin=yml
            else:
                ymax=ymr
            if ymax-ymin<M:
                break
        y=(ymax+ymin)/2
    return x,y
# print (coordiantemeth())

DELTA=10**-3
def dfdx(x,y):
    x1=x-DELTA
    x2=x+DELTA
    f1= f(x1,y)
    f2= f(x2,y)
    dx= x2-x1
    df= f2-f1
    return df/dx
def dfdy(x,y):
    y1=y-DELTA
    y2=y+DELTA
    f1= f(x,y1)
    f2= f(x,y2)
    dy= y2-y1
    df= f2-f1
    return df/dy

def gradf(x,y):
    return dfdx(x,y),dfdy(x,y)

def fastestdescentmeth():
    K=2
    x=X0
    y=Y0
    while abs(x-X_SOL) >= M or abs(y-Y_SOL) >= M:
        gx,gy=gradf(x,y)
        gl=sqrt(gx*gx+gy*gy)
        gx,gy=gx/gl,gy/gl
        gx,gy=-gx,-gy
        xmin=x
        xmax=x+K*gx
        ymin=y
        ymax=y+K*gy
        while True:
            xml=(xmax+xmin*2)/3
            xmr=(xmax*2+xmin)/3
            yml=(ymax+ymin*2)/3
            ymr=(ymax*2+ymin)/3
            if f(xml,yml)>f(xmr,ymr):
                xmin=xml
                ymin=yml
            else:
                xmax=xmr
                ymax=ymr
            if abs(xmax-xmin)<M or abs(ymax-ymin)<M:
                break
        x=(xmax+xmin)/2
        y=(ymax+ymin)/2
    return x,y
print (fastestdescentmeth())

    







        








