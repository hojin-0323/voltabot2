import os

def ismemo(filename):
    name = "memo"+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        return True
    else:
        return False

def openfile(cmd, filename, newfile=False):
    name = cmd+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        with open(name, "r", encoding="utf8") as file:
            return file.read()
    else:
        if newfile:
            with open(name, "w", encoding="utf8") as file:
                file.write('')
                return ''


def editfile(cmd, filename, memo):
    name = cmd+os.path.sep+filename+".txt"
    with open(name, "w", encoding="utf8") as file:
        file.write(memo)

def delfile(cmd, filename):
    name = cmd+os.path.sep+filename+".txt"
    if os.path.isfile(name):
        os.remove(name)

def rev(folder, filename, memo):
    dr = folder+os.path.sep+filename
    revv = 0
    if not os.path.exists(dr):
        os.makedirs(dr)
    else:
        revfile = open(dr+os.path.sep+"rev.txt", "r")
        revv = int(revfile.read())
        revfile.close()
        revv += 1
    revfile = open(dr+os.path.sep+"rev.txt", "w")
    revfile.write(str(revv))
    revfile.close()
    file = open(dr+os.path.sep+"rev{}.txt".format(str(revv)), "w")
    file.write(memo)
    file.close()

def isrev(folder, filename, ver):
    return os.path.isfile(folder+os.path.sep+filename+os.path.sep+"rev{}.txt".format(ver))

def openrev(folder, filename, ver):
    revfile = open(folder+os.path.sep+filename+os.path.sep+"rev{}.txt".format(ver), "r")
    a = revfile.read()
    revfile.close()
    return a

def memover(tp, name, rev):
    return name