import os
for i in range(100, 200):
    os.chdir(f'forward_{i}')
    file_ = open('streams.ocean', "r+")
    f = file_.readlines()
    f = f[0:len(f)-2]
    file_.close()
    file_ = open('streams.ocean', "w")
    file_.writelines(f)
    file_.close()
    os.chdir("..")
