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
            
def memover(tp, name):
    return "볼타봇 메모 서비스 (베타)"