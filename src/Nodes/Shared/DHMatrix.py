

class DHMatrix:
    def __init__(self):
        self.params = {"theta" : {}, "alpha" : {}, "a" : {}, "lambda" : {}}

    def addParam(self, key, val):
        paramType = key[:-1]
        self.params[paramType][key] = val

    def addParams(self, paramsMap):
        for key, val in paramsMap.items():
            self.addParam(key, val)

    def getColSize(self):
        return len(self.params["theta"])