from os import path

f = open("dav_list", "r")
lines = f.readlines()

filenames = []

print(len(lines))
for line in lines:
    line = line.replace("\n", "")
    filenames.append(line)
    print(line)


for file in filenames:
    fp = open(path.join("David", file+".temp"), 'w')
    fp.close()