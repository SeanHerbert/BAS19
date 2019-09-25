import math 

def calcDist(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  
def circleArea(r):
    return (math.pi*r*r)

def iou(r,R,x1,y1,x2,y2):

    d = calcDist(x1,y1,x2,y2)

    if(R < r):
        temp =r
        r = R
        R = temp
    if(d>(r+R)):
        return 0
    part1 = r*r*math.acos((d*d + r*r - R*R)/(2*d*r))
    part2 = R*R*math.acos((d*d + R*R - r*r)/(2*d*R))
    part3 = 0.5*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))
    
    bigCircleArea = circleArea(R)
    smallCircleArea = circleArea(r)

    interArea = part1 + part2 - part3
    if(interArea < 0):
        interArea=0
    
    iou = (interArea/ float(bigCircleArea+smallCircleArea-interArea))
    return iou
