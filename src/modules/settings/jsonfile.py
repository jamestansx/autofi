import json


def write_json(pathToFile, data):
    with open(pathToFile, "w") as outFile:
        json.dump(data, outFile, indent=2)


def read_json(pathToFile):
    with open(pathToFile, "r") as readFile:
        return json.load(readFile)


def update_json(pathToFile, updataData):
    write_json(pathToFile, updataData)
