def getListOfTuples(dictionary, nestedattribute):
    a = []
    for k, v in dictionary.items():
        pair = (k, v[nestedattribute])
        a.append(pair)
    return a