#!/usr/bin/python
# Replaces the binary representations of the target grammar with decimal ones

f = open("COLAG_2011_flat.txt")
lines = f.readlines()
f.close()

f = open("new_COLAG_2011.txt", "w")
for line in lines:
    line = line.replace('"', '').strip()
    alist = line.rsplit('\t',5)
    f.write(str(int(alist[0],2)) + '\t')
    f.write(alist[2] + '\t')
    f.write(alist[3] + '\n')
f.close()
