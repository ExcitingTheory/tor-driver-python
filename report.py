#! /usr/bin/env python3
import glob
import csv
import json
import pprint
import re
import urllib.parse

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
    # Built in, thanks Python: https://docs.python.org/3/library/csv.html
    writer = csv.DictWriter(csvfile, fieldnames=['key', 'num', 'rank', 'orig', 'file', 'name', 'search', 'artifacts'])
    writer.writeheader()
    for searchItem in searchesToProcess:
        if len(searchItem["artifacts"]) >= 1:
            artifacts = searchItem["artifacts"]
            searchItem["artifacts"] = "Multiple see below:"
            writer.writerow(searchItem)
            for link in artifacts:
                _blankRow = blankRow
                data = link.get('data')
                linkName = ""
                if data and len(data) > 0:
                    linkName = data
                else:
                    _link = link.get('link')
                    _parsed = urllib.parse.urlparse(_link)
                    if _parsed.path:
                        linkName = _parsed.path
                    else:
                        linkName = _parsed.netloc
                
                linkName = re.sub(r'"', '', linkName) # Remove double quotes from the link name because it will break the CSV.
                
                # Some examples of making hyperlinks in the stack overflow article https://stackoverflow.com/questions/26928131/how-to-format-hyperlink-in-csv-file-for-excel-import-using-friendly-name 
                _blankRow["artifacts"] = f"=HYPERLINK(\"{link.get('link')}\", \"{linkName}\")"
                writer.writerow(_blankRow)
        else:
            print("No artifacts")
            searchItem["artifacts"] = "None listed"
            writer.writerow(searchItem)
