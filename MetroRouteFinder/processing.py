import json
def dataProcess(Mode=u"InfoCardArray", City=u"Guangzhou"):
    if Mode != "rawJson":
        filename = u"./cache/{City}_{Mode}.json".format(
            City=City, Mode=Mode)
        try:
            k = json.load(open(filename))
        except:
            k = eval(Mode)(City)
            file = open(filename, "w")
            file.write(json.dumps(k))
            file.close()
        return k
    else:
        return json.load(open(u"./data/{City}.json".format(City=City)))