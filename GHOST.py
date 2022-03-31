import os
import sys

import uuid
url = sys.argv[1]
findomain_out = url+".txt"
_dir = uuid.uuid4()
_next_to_print = uuid.uuid4()
_dir_path = os.path.dirname(os.path.abspath(__file__))+"/{}".format(_dir)
print("Finding subdomains...")
os.system('assetfinder {} --subs-only | anew -q domains'.format(url))
os.system('cat domains | httprobe -c 80 | anew -q up')
os.system('findomain -q -t {} -o'.format(url))
os.system('cat {} | anew -q domains | httprobe -c 80 | anew -q up'.format(findomain_out))
print("Enumerating directories...")
with open('up') as file:
    lines = file.readlines()
    os.system('mkdir {}'.format(str(_dir)))
    for line in lines:
        item = line.rstrip('\n')
        os.system('scilla dir -w /usr/share/wordlists/all.txt -target {} -plain | anew {}/{}.txt'.format(item, str(_dir), str(uuid.uuid4())))
os.system('rm -rf up domains {}'.format(findomain_out))
dir_list = os.listdir(_dir_path)
gowitness = open("{}.txt".format(_next_to_print), "x")
for item in dir_list:
    next_path = _dir_path+"/{}".format(item)
    with open(next_path) as file:
        lines = file.readlines()
        if len(lines)>0:
            for url in lines:
                with open("{}.txt".format(_next_to_print), "a") as file:
                    file.write("{}\n".format(url.rstrip('\n')))
print("Taking pictures...")
os.system('gowitness file -t 8 -f {}.txt --disable-logging --disable-db --delay 10 --timeout 15'.format(_next_to_print))
print("Done.")
os.system('rm -rf {}/ {}.txt'.format(_dir_path, _next_to_print))