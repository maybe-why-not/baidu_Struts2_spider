#!/usr/bin/env Python
# coding=utf-8
import time
import urllib.request
import re
import requests

file = 'S2过滤action3.txt'
urls = 1000000
content_code = urllib.request.quote('inurl:*.action?')  #解决中文编码的问题

f = open('action_regex.txt','r',encoding='utf-8')
regex_list = f.readlines()
last = len(regex_list)
f.close()
mark = len(regex_list)
url1 = 'https://www.baidu.com/s?wd='
url2 = '&pn='
url3 = '&oq=inurl%3A%2A.action%3F&rn=50&ie=utf-8&rsv_pq=f55638080004c2b8&rsv_t=b0a1OQokSTULwF8ASK9ClOgiY6xOpu4Uhc71pp9Mq1VIKj80NmFcfiR8NVo'

for canshu in range(297, int(urls/550)):
    for page in range(50, 600, 50):
        url = url1 + content_code + '%20' + str(canshu) + url2 + str(page) + url3
        print(url)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
        response = urllib.request.urlopen(req)
        
        try:
            html = response.read().decode('utf-8')

        except:
            pass
        
        else:

            link_list = re.findall(r'<a target="_blank" href="(.*?)" class="c-showurl" style="text-decoration:none;">', html)  

            f = open(file,'a',encoding='utf-8')

            for url in link_list:    

                response = requests.get(url, allow_redirects=False)

                craw_context = response.headers.get('location')

                if craw_context:#空链接跳过
                    continue
                
                craw_context = craw_context.lower()
                position = [i.start() for i in re.finditer('/', craw_context)]
                if len(position) >2:
                    behind = craw_context[position[2]:len(craw_context)]
                    if re.search('([\.|\?|&]action[\?|=])|(\.action$)',behind):
                        
                        craw_context_regex = craw_context
                        value = [i.start() for i in re.finditer('=', craw_context_regex)]

                        if value:
                            
                            value1 = [i.start() for i in re.finditer('\.|\/|\:|\?|\&', craw_context_regex)]
                            
                            if value1[-1] < value[-1]:
                                        craw_context_regex = craw_context_regex[:value[-1]+1] + '\n'
                                        
                            for i in reversed(value):
                                for j in value1:
                                    if j > i:
                                        craw_context_regex = craw_context_regex[0:i+1] + craw_context_regex[j:]
                                        break

                        strlist = re.split('\.|\/|\:|\?|=|\&',craw_context_regex)
                        
                        for i in strlist:
                            if len(i)>20:
                                craw_context_regex=craw_context_regex.replace(i,'')

                        regex = craw_context[0:position[2]] + re.sub(r'([\d]+)','',craw_context_regex[position[2]:len(craw_context_regex)]) + ' '
                        
                        if (regex in regex_list) or ((regex+'\n') in regex_list):
                            continue
                        
                        else:
                            regex_list.append(regex)
                            f.write(craw_context + '\n')
                            f2 = open('action_regex.txt','a',encoding='utf-8')
                            f2.write(regex)
                            f2.close()

            f.close()
            print(str(round((page+(canshu*550))/urls,4)*100) + '%')
            time.sleep(1)

            if (page+(canshu*550))%40000 == 0:
                print('---------反爬暂停15分钟---------')
                time.sleep(900)
        
    if mark == len(regex_list):
        print('------------警告-----------此轮无新链接采集--------------------')
    else:
        print('已采集 ' + str(len(regex_list)-last) + ' 条,此轮增加 ' + str(len(regex_list)-mark) + ' 条')
        mark = len(regex_list)
        
print('链接采集去重完毕,共 ' + str(len(regex_list)) + ' 条')
