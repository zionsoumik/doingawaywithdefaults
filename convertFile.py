#!/usr/bin/python
# Converts the original language file into
# a format more usable to the program

f = open("EngFrJapGerm_original.txt","r")
lines = f.readlines()
f.close()

f = open("EngFrJapGerm.txt","w")
for line in lines:
    line = line.replace('"', '').strip()
    alist = line.rsplit('\t',5)
    f.write(alist[0] + '\t')
    f.write(alist[2] + '\t')
    f.write(alist[3] + '\n')
f.close()