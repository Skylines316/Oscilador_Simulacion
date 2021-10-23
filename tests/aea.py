#funcion que retorna un resorte dinamico
def spring(xo,yo,xf,yf,width,points):
    cicle=(-1,1)
    j=0
    i=1
    total_points=points+4
    x=[xo,xo]
    y=[yo,yo+i/total_points*(yf-yo)]
    while i<total_points:
        if total_points-i<=2:
            x.append(xf)
        else:
            x.append(xo+(i%2*2-1)*width)
        y.append(yo+i/total_points*(yf-yo))
        i+=1

    return x, y

x, y = spring(0,0,0,100,1,50)
print(len(x),len(y))
print(x)