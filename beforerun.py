import timeinfo

build = 0
day = "000000.000000"
versionm = "1.0"

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

def varset(doUpdate): # 변수 설정
    global build
    global day
    global versionm

    versionlogfile = open("versioninfo.txt", "r", encoding="utf8")
    versionm = versionnum(versionlogfile)
    versionlogfile.close()
    bld = 0

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