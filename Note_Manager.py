the_file = []
with open("Python.html") as f:
    for line in f:
        the_file.append(line)

with open("Python_Edited.html", mode='a') as y:
    for line in the_file:
        y.write(line)
