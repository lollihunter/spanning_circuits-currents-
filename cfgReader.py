def cfgread():
    with open("cfg/settings.cfg") as a:
        a = a.readlines()
        d = {}
        for i in a:
            i = i.split("=")
            d[i[0].strip()] = float(i[1].strip()) if '.' in i[1] else int(i[1].strip())
    return d