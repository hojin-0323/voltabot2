import time

def yy(x):
    resstr=str(x)
    rstr = resstr[len(resstr)-2:]
    while len(rstr) != 2:
        rstr = "0" + rstr
    return rstr

def timestr(): # 시간 정보를 출력합니다. 
    name = time.localtime()
    return yy(name[0])+yy(name[1])+yy(name[2])+"."+yy(name[3])+yy(name[4])+yy(name[5])