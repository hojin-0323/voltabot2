import timeinfo
import os

sp = os.path.sep

build = 0
day = "000000.000000"
versionm = "1.0"
token = ""
versioncode = ""

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

def getversioncode(doUpdate, isBeta):
    maincodefile = open("res{0}version{0}versioncode{0}maincode.txt".format(sp), "r")
    vercode = maincodefile.read()
    releasenumfile = open("res{0}version{0}versioncode{0}releasenum.txt".format(sp), "r")
    releasenum = int(releasenumfile.read())
    releasenumfile.close()
    releasenumfile = open("res{0}version{0}versioncode{0}releasenum.txt".format(sp), "w")
    if doUpdate:
        releasenumfile.write(str(releasenum+1))
        releasenum += 1
    else:
        releasenumfile.write("0")
        releasenum = 0
    releasenumfile.close()
    if releasenum:
        return vercode + " test release " + str(releasenum)
    elif isBeta:
        return vercode + " final release"
    else:
        return vercode

def varset(doUpdate, isBeta): # 변수 설정
    global build
    global day
    global versionm
    global token
    global versioncode

    pyset = open("test.py", "w", encoding="utf8")
    pyset.write("")
    pyset.close()

    versionlogfile = open("res"+sp+"versioninfo.txt", "r", encoding="utf8")
    versionm = versionnum(versionlogfile)
    versionlogfile.close()
    versioncode = getversioncode(doUpdate, isBeta)
    bld = 0 
    tokenfile = open("res"+sp+"security"+sp+"token.txt", "r")
    token = tokenfile.read()
    file = open("res{}botbuild.txt".format(sp), "r")
    bld = int(file.read())
    file.close()
    if doUpdate:
        file = open("res{}botbuild.txt".format(sp), "w")
        file.write(str(bld+1))
        build = bld+1
        file = open("res{}botbuildday.txt".format(sp), "w")
        day = timeinfo.timestr()
        file.write(day)
        file.close()
    else:
        build = bld
        file = open("res{}botbuildday.txt".format(sp), "r")
        day = file.read()
        file.close()