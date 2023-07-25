import os, re
for i in range(0, 518):
    os.chdir(f'forward_{i}')
    item = "streams.ocean"
    with open(item, mode = "r+") as file:
        file_text = file.read()
        regex = re.compile("overwrite")
        file_text = regex.sub("truncate", file_text)
        file.seek(0)
        file.write(file_text)
        file.close()
    os.chdir('..')
