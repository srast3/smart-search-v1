import json

class Utilities:
    @staticmethod
    def getJsonDataFromFile(fileName):
        file = open(fileName)
        jsonData = json.load(file)
        return jsonData
