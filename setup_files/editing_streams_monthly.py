import os, re
for i in range(0, 518):
    os.chdir(f'forward_{i}')
    item = "streams.ocean"
    with open(item, mode = "r+") as file:
        file_text = file.read()
        regex = re.compile("01-00-00_00:00:00")
        file_text = regex.sub("00-01-00_00:00:00", file_text)
        file.seek(0)
        file.write(file_text)
        file.close()
    os.chdir('..')
