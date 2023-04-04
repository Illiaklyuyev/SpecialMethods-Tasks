from math import exp,sqrt,cos,sin

# f=open ("fit_Dm_1.dat")
f=open ("fit_Dm_4.dat")
lines=f.readlines ()
f.close()
points=[]
for line in lines:
    x,y=line.split("\t")
    y=y.replace("\n","")
    x=x.replace(",",".")
    y=y.replace(",",".")
    x=float(x)
    y=float(y)
    points.append((x,y))
    # print (x,y)
# print(points) 

# def f(x,a,b,c,d):
#     return a*exp(-b*(x-c))+d

# def f(x,a,b,c,d):
#     return a*cos(b*(x-c))+d

def f(x,a,b,c,d,e,ef,g):
    return a*exp(-((x-b)/c)**2)+d*exp(-((x-e)/ef)**2)+g

def errorfunc(a,b,c,d,e,ef,g):
    global points
    sum=0
    for point in points:
        x,y=point
        y_sequel=f(x,a,b,c,d,e,ef,g)
        dy=y_sequel-y
        sum+=dy**2
    return sqrt(sum)
# print(errorfunc(1,1,1,0))

def hooke_jeeves_meth():
    a=0
    b=0
    c=0.1
    d=0
    e=0
    ef=0.1
    g=0
    alpha=1.5
    beta=1/alpha
    step=1
    while step>10**-4:
        f_here=errorfunc(a,b,c,d,e,ef,g)
        fa_plus =errorfunc(a+step,b,c,d,e,ef,g)
        fa_minus=errorfunc(a-step,b,c,d,e,ef,g)
        fb_plus =errorfunc(a,b+step,c,d,e,ef,g)
        fb_minus=errorfunc(a,b-step,c,d,e,ef,g)
        fc_plus =errorfunc(a,b,c+step,d,e,ef,g)
        fc_minus=errorfunc(a,b,c-step,d,e,ef,g)
        fd_plus =errorfunc(a,b,c,d+step,e,ef,g)
        fd_minus=errorfunc(a,b,c,d-step,e,ef,g)
        fe_plus =errorfunc(a,b,c,d,e+step,ef,g)
        fe_minus=errorfunc(a,b,c,d,e-step,ef,g)
        fef_plus =errorfunc(a,b,c,d,e,ef+step,g)
        fef_minus=errorfunc(a,b,c,d,e,ef-step,g)
        fg_plus =errorfunc(a,b,c,d,e,ef,g+step)
        fg_minus=errorfunc(a,b,c,d,e,ef,g-step)
        f_list=[f_here,fa_plus,fa_minus,fb_plus,fb_minus,fc_plus,fc_minus,fd_plus,fd_minus,fe_plus,fe_minus,fef_plus,fef_minus,fg_plus,fg_minus]
        index_min = min(range(len(f_list)), key=f_list.__getitem__)
        if index_min==0:
            step*=beta
        elif index_min==1:
            a+=step
            step*=alpha
        elif index_min==2:
            a-=step
            step*=alpha
        elif index_min==3:
            b+=step
            step*=alpha
        elif index_min==4:
            b-=step
            step*=alpha
        elif index_min==5:
            c+=step
            step*=alpha
        elif index_min==6:
            c-=step
            step*=alpha
        elif index_min==7:
            d+=step
            step*=alpha
        elif index_min==8:
            d-=step
            step*=alpha
        elif index_min==9:
            e+=step
            step*=alpha
        elif index_min==10:
            e-=step
            step*=alpha
        elif index_min==11:
            ef+=step
            step*=alpha
        elif index_min==12:
            ef-=step
            step*=alpha
        elif index_min==13:
            g+=step
            step*=alpha
        elif index_min==14:
            g-=step
            step*=alpha
        else:
            raise IndexError
    return a,b,c,d,e,ef,g 
print (hooke_jeeves_meth())    



