import os, re
for i in range(100, 200):
    os.chdir(f'forward_{i}')
    item = "streams.ocean"
    with open(item, mode = "r+") as file:
        file_text = file.read()
        regex = re.compile("0003-00-00_00:00:00")
        file_text = regex.sub("0001_00:00:00", file_text)
        file.seek(0)
        file.write(file_text)
        file.close()
    os.chdir('..')
