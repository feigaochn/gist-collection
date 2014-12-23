def fr2fc(a,b,t):
    "Return continuos fraction fc0 [a1,a2,a3,...at] from a fraction a/b"
    a=float(a);b=float(b);t0=0
    fc0=[];c=(a/b);pe=int(c);pf=c-pe
    while (t0 < t):
        fc0.append(pe);t0+=1
        c=1.0/pf;pe=int(c);pf=c-pe
    return fc0

def fc2dec(fc0):
    "Return a number from a continuos fraction fc0 [a1,a2,a3,...]"
    ff=list(fc0); ff.reverse()
    return reduce(lambda x,y: y+(1.0/x),ff)

def fc2fr(fc0):
    "Return a fraction from a continuos fraction fc0 [a1,a2,a3,...]"
    fc3=list(fc0)
    s2=[fc3.pop(),1]
    fc3.reverse()
    for k in fc3:
        s2.reverse()
        s2=[k*s2[1]+s2[0],s2[1]]
    return s2

if __name__ == "__main__":

    f1= fr2fc(3.141516,1,10)
    print f1

    for k in range(1,len(f1)+1):
        f2= fc2fr(f1[0:k]);print f1[0:k],f2 ,float(f2[0])/f2[1]

    print fc2dec(f1)