import os
import urllib2
import time
import json

#
#  Reads from a file called simple, which is a dump of https://pypi.python.org/simple/
#
#  Extracts URLs from that file, queries the web for info about each package
#  and writes into info.json the following structure:
#
#  {"rawname":"2c.py",
#   "name":"2C.py",
#   "num_releases":2,
#   "downloads":{
#       "last_month":5,
#       "last_week":0,
#       "last_day":0},
#   "urls":[
#       "http://code.google.com/p/2c-python/",
#       "http://code.google.com/p/2c-python/downloads/"
#   ],
#   "num_releases_2015":0},
#

info = open("info.json", "w")
info.write("[")
simp = open("simple", "r")
for line in simp:
    if line[:9] == "<a href='":
        rawname = line.split("'")[1]
        print rawname
        try:
            time.sleep(.5)
            url = "http://pypi.python.org/pypi/" + rawname + "/json/"
            print url
            response = urllib2.urlopen(url)
            theresp = response.read()
            if not os.path.exists("cache/" + rawname[0]):
                os.makedirs("cache/" + rawname[0])
            with open("cache/" + rawname[0] + "/" 
                        + rawname + ".json", "w") as f:
                f.write(theresp)
            thejson = json.loads(theresp)
            releases = thejson["releases"].keys()
            releases2015 = [k for k in releases if
                 len(thejson["releases"][k]) > 0 and
                 thejson["releases"][k][0]["upload_time"][:4] == "2015"]
            urls = [thejson["info"]["home_page"],
                    thejson["info"]["docs_url"], 
                    thejson["info"]["download_url"], 
                    thejson["info"]["package_url"], 
                    thejson["info"]["bugtrack_url"]] 
            urls = [u for u in urls if u is not None 
                        and "http:" in u 
                        and "pypi.python" not in u]
            nicename = thejson["info"]["name"]
            downloads = thejson["info"]["downloads"]
            print "\t",len(releases), "releases", len(releases2015), "in 2015"
            info.write(json.dumps({"rawname":rawname, 
                                   "name":nicename,
                                   "num_releases":len(releases),
                                   "num_releases_2015":len(releases2015),
                                   "urls":urls,
                                   "downloads":downloads},
                                   separators=(',',':')) + ",\n")
        except Exception, e:
            print "ERROR:", line, type(e), e
