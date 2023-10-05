import os

a = "123abc"
b = int("0x"+a, 16)
print(hex(b))

def open_res(filename):
    name = "res{}".format(os.path.sep)+filename+".txt"
    with open(name, "r", encoding="utf8") as file:
        return file.read()

print(open_res("versioninfo"))