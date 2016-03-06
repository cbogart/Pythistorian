import os
import urllib2
import time
import json
from dateutil.parser import parse
import csv

relevant_versions = open("pypi_github_v2015.csv", "r")
info = json.load(open("info.json", "r"))
vercsv = csv.writer(open("pypi_versions.csv", "w"))
vercsv.writerow(["project_owner","project_name","pypi_name", "pypi_rawname","version","upload_time","python_version", "filename"])

for line in relevant_versions:
    line = line.strip()
    print line
    (gitproject, nicename) = line.split(",")
    infoline = [i for i in info if i["name"] == nicename]
    print "\tfound:", len(infoline), [i["rawname"] for i in infoline]
    if len(infoline) == 1:
        rawname = infoline[0]["rawname"]
        allinfo =  json.load(open("cache/" + rawname[0] + "/" + rawname + ".json", "r"))
        for rel in allinfo["releases"]:
            for rec in allinfo["releases"][rel]:
                 vercsv.writerow([gitproject.split("/")[0],
                                  gitproject.split("/")[1], nicename, rawname, rel, 
                                  parse(rec["upload_time"]), rec["python_version"], rec["filename"]])
