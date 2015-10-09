import os

def wise_mk_dir(path):
    if path == "":
        return
    if os.path.exists(path):
        return
    p, c = os.path.split(path)
    if not os.path.exists(p):
        wise_mk_dir(p)
    os.mkdir(path)