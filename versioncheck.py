import os

def versionnum(file):
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

def ischanged(filepath, logd):
    file = open(filepath, "r", encoding='utf8')
    log = ""
    for line in file.readlines():
        log = log + line
    file.close()
    if log == logd:
        return False
    else:
        return True

def logcheck(filepath, log, ver, build, date):
    if ischanged(filepath, log):
        file = open(filepath, "w", encoding='utf8')
        logdefault = open("versioninfodefault.txt", "r", encoding="utf8")
        versionlogfile = open("versionupdatelog"+os.path.sep+ver+"."+str(build)+".txt", "w", encoding="utf8")
        file.write(log)
        logtext = logdefault.read().replace("[버전명]", ver).replace("[빌드번호]", str(build)).replace("[버전명]", ver).replace("[빌드날짜]", date).replace("[변경사항]", log)
        versionlogfile.write(logtext)
        file.close()
        versionlogfile.close()
        logdefault.close()
        print("변경 사항 저장됨")
        return log
    else:
        print("변경 사항 없음")
        return "변경 사항 없음"

vernew = "*관리자 전용*\n띵킹"
file = open("versionlogbuffer.txt", "r", encoding='utf8')

logcheck("versionlogbuffer.txt", vernew, "1.95", 48, "721121.000000")