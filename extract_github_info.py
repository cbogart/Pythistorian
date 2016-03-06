#import read_ga
from dateutil.parser import parse
from datetime import timedelta
import json
import sys
import datetime
#import jsonpath_rw
import csv
import re

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

csvwriter = csv.writer(sys.stdout)
errors = open("errs.txt", "w")
gitr = re.compile(ur'github\.[a-z]{3}/([^/\., \r\n\t"]+)/([^/, \r\n\t"]+?)[,/ "]')
#gitalt = re.compile(ur'git@github.com:([^/\., \r\n\t]+)/([^/, \r\n\t]+?)[,/ "]')
gitalt2 = re.compile(ur'/([^/\., \r\n\t"]+).github.[a-z]{2,3}/([^/, \r\n\t"]+?)[/ ",]')
#csvreader = csv.reader(sys.stdin)
data = json.load(sys.stdin)
for jsline in data:
    try:
       projname = jsline["name"]

       line = json.dumps(jsline)
       if "github" in line and jsline["num_releases_2015"] > 2:
           gh = gitr.search(line)
           if gh is None:
               gh = gitalt2.search(line)
           if gh is not None:
               user = gh.group(1)
               proj = gh.group(2)
               if proj[-4:] == ".git":
                   proj = proj[:-4]
               csvwriter.writerow((user + "/" + proj, projname))
           else:
               try:
                   gitloc = re.search(r"github", line).start(0)
                   errors.write(line[gitloc:]+ line+ "\n")
               except:
                   errors.write( "WAAAA: can't find github in "+ line+ "\n")
           #csvwriter.writerow([gh[0].encode('utf8') if isinstance(v,unicode) else v for v in ch])
           #csvwriter.writerow([gh[0].encode('utf8') if isinstance(gh[0],unicode) else gh[0]])
    except UnicodeEncodeError, uee:
       sys.stderr.write( str(len(line)) + "//" + line + "//" + str(uee))
       raise uee
#    except ValueError, ve:
#       sys.stderr.write(line, ve)
#       raise uee
