import os, re
for i in range(100, 200):
    os.chdir(f'forward_{i}')
    item = "namelist.ocean"
    with open(item, mode = "r+") as file:
        file_text = file.read()
        regex = re.compile("config_do_restart = .false.")
        file_text = regex.sub("config_do_restart = .true.", file_text)
        file.seek(0)
        file.write(file_text)
        file.close()
    os.chdir('..')
