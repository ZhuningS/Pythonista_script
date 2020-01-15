# -*- coding: utf-8 -*-
import re
import requests
import json
import urllib.request
import urllib.error
import os
import sys

minimumsize = 10
if len(sys.argv)<=1:
	musicId = input("复制网易云歌单链接地址:")
	if musicId.find("music.163.com")< 0:
		musicId = "http://music.163.com/#/playlist?id="+musicId
else:
	musicId = sys.argv[1]
print("fetching msg from %s \n" % musicId)
url = re.sub("#/", "", musicId).strip()
print(url)
r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'})
contents = r.text
res = r'<ul class="f-hide">(.*?)</ul>'
mm = re.findall(res, contents, re.S | re.M)
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
if(mm):
    contents = mm[0]
else:
    print('Can not fetch information form URL. Please make sure the URL is right.\n')
    os._exit(0)

res = r'<li><a .*?>(.*?)</a></li>'
mm = re.findall(res, contents, re.S | re.M)

for value in mm:
    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    value = value.replace('\\xa0', ' ')# windows cmd 的编码问题
    print(value)

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if d is not None and 'data' not in d:
        continue
    songid = d["data"]["song"][0]["songid"]
    print("find songid: %s" % songid)

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'flac'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if('data' not in d) or d['data'] == '':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    print("find songlink: ")
    if(len(songlink) < 10):
        print("\tdo not have flac\n")
        continue
    print(songlink)

    songdir = "songs_dir"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    
    songname = songname.replace('/', "%2F").replace('\"', "%22")
    
    filename = ("%s/%s/%s-%s.flac" %
                (CURRENT_PATH, songdir, songname, artistName))

    f = urllib.request.urlopen(songlink)
    headers = requests.head(songlink).headers
    if 'Content-Length' in headers:
        size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
    else:
        continue

    #Download unfinished Flacs again.
    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize: #Delete useless flacs
        print("%s is downloading now ......\n\n" % songname)
        if size >= minimumsize:
            with open(filename, "wb") as code:
                code.write(f.read())
        else:
            print("the size of %s (%r Mb) is less than 10 Mb, skipping" %
                  (filename, size))
    else:
        print("%s is already downloaded. Finding next song...\n\n" % songname)


print("\n================================================================\n")
print("Download finish!\nSongs' directory is %s/songs_dir" % os.getcwd())
