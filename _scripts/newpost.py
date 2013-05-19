import os
import datetime
import sys
import subprocess

def defaultcontent(title):
   default = "---\nlayout: post\ntitle: {0}\n---\n".format(title)
   return default

title = " ".join(sys.argv[1:])
titleDashed = title.replace(' ', '-')
date = datetime.date.today().strftime("%Y-%m-%d")
filename = "/Users/chris/blog/didurestart/_posts/%s-%s.md" % (date, titleDashed)
print("creating file {0}".format(filename))
with open(filename, 'w') as f:
    f.write(defaultcontent(title)) 

subprocess.call("vim '{0}'".format(filename), shell=True)
