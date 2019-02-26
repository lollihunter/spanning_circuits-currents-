def cfgRead(): # translate text from config into dictionary
    
    d = {}
    with open("cfg/settings.cfg") as a:
        a = a.readlines()
        for line in a:
            line = line.split("=")
            d[line[0].strip()] = getType(line[1].strip())
    return d


def getType(data): # guess data type by analyzing string characteristics
    
    if data.isdigit():
        return int(data)
    elif data.replace('.', '').isdigit():
        return float(data)
    else:
        return data
    
    
def overrideConfig(default, config): # try to override default values with ones from .cfg
    
    for key in default:
        try:
            default[key] = config[key]
        except KeyError:
            pass