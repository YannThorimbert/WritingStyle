import os
import odt2txt
import re

to_find = "nul"
occurences = {}
for folder, subfolders, files in os.walk("./"):
    for file in files:
        if file.endswith(".odt"):
            print(file)
            fn = os.path.join(folder, file)
            odt = odt2txt.OpenDocumentTextFile(fn)
            unicode = odt.toString()
            occurences[fn] = [m.start() for m in re.finditer(to_find, unicode)]


