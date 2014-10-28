# read config from ini file

import ConfigParser


def getSections(filename):
    Config = ConfigParser.ConfigParser()
    Config.read(filename)
    return Config.sections()    

def getConfigSection(filename, section):
    Config = ConfigParser.ConfigParser()
    Config.read(filename)
    sectiondict = {}
    options = Config.options(section)
    for option in options:
        try:
            sectiondict[option] = Config.get(section, option)
            if sectiondict[option] == -1:
                DebugPrint("skip: %s in section %s" % (option, section))
        except:
            print("exception on %s in section %s!" % (option, section))
            sectiondict[option] = None
    return sectiondict

