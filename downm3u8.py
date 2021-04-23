# codeing=utf-8
import requests
from os import makedirs, remove
from re import sub
from time import time
import os
import re
import sys

ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 dingtalk-win/1.0.0 nw(0.14.7) DingTalk(6.0.12-Release.4190287) Mojo/1.0.0 Native AppType(release) Channel/201200'}


def dl_aria2(url, dir, name):
    os.system(f"aria2c -o {name} --dir={dir} \"{url}\"")


def dl_request(url, dir, name):
    r = requests.get(url, headers=ua)
    with open(dir+name, "wb") as code:
        code.write(r.content)


requests.packages.urllib3.disable_warnings()
x = requests.session()

tmp = input('URL: ')

pattern2 = re.compile('\w{8}(-\w{4}){3}-\w{12}')
pattern1 = re.compile('\S*://\S+.alicdn.com/.*?/')

name = re.search(pattern2, tmp).group(0)
host = re.search(pattern1, tmp).group(0)
path = 'download/temp/' + name + "/"
n = 0
total = 0
try:
    makedirs(path)
except:
    pass

dl_request(tmp, path, name+".m3u8")
filem3u8 = open(path+name+'.m3u8')

while True:
    tp2 = filem3u8.readline()
    if tp2 == '':
        break
    if tp2.startswith('#'):
        continue
    total += 1

filem3u8.seek(0)

# 下载
while True:
    try:
        tp2 = filem3u8.readline()
        if tp2 == '':
            print('Finished!')
            break
        if tp2.startswith('#'):
            continue
        # print(tp2)
        tp2 = tp2.strip()
        print(f'Downloading [{n+1}/{total}] ...', end='')
        sys.stdout.flush()
        dl_request(host+tp2, path, f"{n+1}.ts")
    except Exception as e:
        print(f'Fail to download {n+1}.ts \n {e}')
        break
    n += 1
    print('[done]')

# 整合
print('Combining...')
p = f'{path}{name}_{int(time())}.ts'
with open(p, 'wb') as f:
    for i in range(n):
        with open(f'{path}{i+1}.ts', 'rb') as tmp:
            f.write(tmp.read())
        remove(f'{path}{i+1}.ts')

# 删除无用文件
filem3u8.close()
f.close()
# remove(f'{path}{name}.m3u8')

a = input('Done. Press enter to exit.')
