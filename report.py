#! /usr/bin/env python3
import glob
import csv
import json
import pprint

searchesToProcess = []
blankRow = {
    'key': '',
    'num': '',
    'rank': '',
    'orig': '',
    'file': '',
    'name': '',
    'search': '',
    'artifacts': ''
}

for name in glob.glob('./results/*.json'):
    with open(name, "r") as fileHandler:
        print(name)
        fileLines = fileHandler.readlines()
        searchesToProcess.append(json.loads(fileLines[0])) # TODO - Loop through all lines if there are more than one, i.e. jsonl files.

with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['key', 'num', 'rank', 'orig', 'file', 'name', 'search', 'artifacts'])
    writer.writeheader()
    for searchItem in searchesToProcess:
        if len(searchItem["artifacts"]) >= 1:
            _artifacts = searchItem["artifacts"]
            searchItem["artifacts"] = "Multiple see below:"
            writer.writerow(searchItem)
            for link in _artifacts:
                _blankRow = blankRow
                _blankRow["artifacts"] = f"=HYPERLINK(\"{link.get('link')}\", \"{link.get('data')}\")"
                writer.writerow(_blankRow)
        else:
            print("No artifacts")
            searchItem["artifacts"] = "None listed"
            writer.writerow(searchItem)
