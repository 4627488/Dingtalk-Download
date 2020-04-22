#codeing=utf-8
from requests import session, packages
from os import makedirs, remove
from re import sub
from time import time
import os
import re
import sys

packages.urllib3.disable_warnings()
x = session()

tmp = input('URL: ')

pattern2 = re.compile('\w{8}(-\w{4}){3}-\w{12}')
pattern1 = re.compile('\S*://\S+.alicdn.com/.*?/')

name = re.search(pattern2,tmp).group(0)
host = re.search(pattern1,tmp).group(0)
path = './download/temp/'+ name +"/"
head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 dingtalk-win/1.0.0 nw(0.14.7) DingTalk(5.0.15-Release.23) Mojo/1.0.0 Native AppType(release)'}
n = 0
total=0
try: makedirs(path)
except: pass
end = b'<Code>NoSuchKey</Code>'

re = x.get(tmp,headers=head, verify=False)
ff = open(path+name+'.m3u8','wb') 
ff.write(re.content)
ff.close()

filem3u8=open(path+name+'.m3u8')

while True:
    tp2=filem3u8.readline()
    if tp2=='':
        break
    if tp2.startswith('#'):
        continue
    total+=1

filem3u8.seek(0)
# 下载
while True:
    try:
        tp2=filem3u8.readline()
        if tp2=='':
            print('Finished!')
            break
        if tp2.startswith('#'):
            continue
        #print(tp2)
        tp2=tp2.strip();
        print(f'Downloading [{n+1}/{total}] ...',end='')
        sys.stdout.flush()
        re = x.get((host+tp2), headers=head, verify=False)
    except Exception as e:
        print(f'Fail to download {n+1}.ts due to {e}')
        break        
    with open(f'{path}{n+1}.ts','wb') as f:
        f.write(re.content)
    n+=1
    print('[done]')

# 整合
print('Combining...')
p = f'{path}{name}_{int(time())}.ts'
with open(p, 'wb') as f:
    for i in range(n):
        with open(f'{path}{i+1}.ts', 'rb') as tmp:
            f.write(tmp.read())
        remove(f'{path}{i+1}.ts')

# 转换
pp =  './download/'+name+'.mp4'
os.system('ffmpeg.exe -i '+p+' '+pp)

#删除无用文件
filem3u8.close()
f.close()


a = input('Done. Press enter to exit.')