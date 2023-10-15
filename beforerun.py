import timeinfo
import os

sp = os.path.sep

build = 0
day = "000000.000000"
versionm = "1.0"
token = ""
versioncode = ""

class VersioncodeUpdate(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def versionnum(file): # 버전 정보 가져오는 함수
    versionline = ""
    versionsplitcount = 0
    versionstring = ""
    for line in file.readlines():
        if line[:3] == "ver":
            versionline = line
            break
    for i in range(len(versionline)):
        if versionline[i] == ".":
            versionsplitcount += 1
        if versionsplitcount >= 2:
            break
        versionstring = versionstring + versionline[i]

    return versionstring[4:]

def varset(doUpdate, vsc): # 변수 설정
    global build
    global day
    global versionm
    global token
    global versioncode

    versionlogfile = open("res"+sp+"versioninfo.txt", "r", encoding="utf8")
    versionm = versionnum(versionlogfile)
    versionlogfile.close()
    vscfile = open("res"+sp+"versioncode.txt", "r")
    prevvsc = vscfile.read()
    vscfile.close()
    if doUpdate:
        if prevvsc == vsc:
            raise VersioncodeUpdate("버전 코드를 업데이트하세요.")
        else:
            vscfile = open("res"+sp+"versioncode.txt", "w")
            vscfile.write(vsc)
            vscfile.close()
    bld = 0 
    tokenfile = open("res"+sp+"security"+sp+"token.txt", "r")
    token = tokenfile.read()
    file = open("botbuild.txt", "r")
    bld = int(file.read())
    file.close()
    if doUpdate:
        file = open("botbuild.txt", "w")
        file.write(str(bld+1))
        build = bld+1
        file = open("botbuildday.txt", "w")
        day = timeinfo.timestr()
        file.write(day)
        file.close()
    else:
        build = bld
        file = open("botbuildday.txt", "r")
        day = file.read()
        file.close()