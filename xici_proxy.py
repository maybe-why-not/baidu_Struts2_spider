import requests, re, time, random, os, lockfile
from bs4 import BeautifulSoup
import threading, queue
from requests.packages import urllib3
urllib3.disable_warnings()

class proxy_check(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        global filename, proxy_list, ip_list, keys, count
        while  not self._queue.empty():
            page = self._queue.get()
            url = 'https://www.xicidaili.com/nn/' + str(page)

            header = {'User-Agent': keys[random.randint(0, len(keys) - 1)],
                      'Host': 'www.xicidaili.com',
                      'Cache-Control': 'max-age=0',
                      'Upgrade-Insecure-Requests': '1',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate',
                      'Accept-Language': 'zh-CN,zh;q=0.9',
                      'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWE2NGRhNDVlMzJkNTc4OGViY2FiZGZkMjc2ZGJiNGM5BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTBxeTF0VU1nek1TVXREMGZ4SnlsZTZtMnpiTU43c1krUXV5NWtuZ2NEYzg9BjsARg%3D%3D--917db1f8cf491a8edfb3f1671e45c1795092db4c; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1542621487,1542627625,1542674143; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=',
                      'Connection': 'close'
                      #'If-None-Match': 'W/"fb7acc2d9cf0d588d69658c294207254"'
                     }

            for i in range(0,3):
                try:
                    r = requests.get(url=url, headers=header)#, proxies={'https':'http://127.0.0.1:1080'})#, proxies={'http':'http://27.155.84.233:8081'})
                    html = r.text
                    if r.status_code == 200:
                        break
                    else:
                        time.sleep(5 + float(random.randint(1,100)) /20)
                except:
                    time.sleep(5 + float(random.randint(1,100)) /20)
            
            if html:    
                soup = BeautifulSoup(html, 'lxml')
                middle_check = soup.find(id='ip_list')
                if middle_check:
                    ips = middle_check.find_all('tr')
                    print ('第 ' + str(page) + ' 页，' + str(len(ips)-1) + ' 个ip正在尝试...')
                    for j in range(1, len(ips)):
                        ip_info = ips[j]
                        tds = ip_info.find_all('td')
                        divs = ip_info.find_all("div", {"class":"bar_inner fast"})
                        if len(divs)==2:
                            proxy =  tds[1].text + ':' + tds[2].text
                            with open('proxy','a',encoding='utf-8') as f:
                                file_lock = lockfile.MkdirFileLock(filename)    
                                while(1):
                                    try:
                                        file_lock.acquire()
                                    except:
                                        time.sleep(0.1)
                                    else:
                                        break
                                f.write('<Proxy US 0.00s [] ' + proxy + '>\n')
                                file_lock.release()
                                            
                else:
                    print ('[' + str(r.status_code) + '] ' + '第 ' + str(page) + ' 页返回内容没有ips标签')
                    with open('异常.txt','a',encoding='utf-8') as f:
                        file_lock = lockfile.MkdirFileLock(filename)    
                        while(1):
                            try:
                                file_lock.acquire()
                            except:
                                time.sleep(0.1)
                            else:
                                break
                        f.write(html)
                        file_lock.release()

            else:
                print ('[' + str(r.status_code) + '] ' + '第 ' + str(page) + ' 页返回html为空')

            time.sleep(0 + float(random.randint(1,100)) /20)
            #print("第{}页代理列表抓取成功.".format(i))

def main():

    threads = []
    Queue = queue.Queue()

    start_time = time.clock()
    print("正在获取代理列表...")
    
    for i in range(1,pages+1):
        Queue.put(i)
        
    for i in range(threads_count):
        threads.append(proxy_check(Queue))	
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return start_time

if __name__ == '__main__':
    pages = 100
    threads_count = 3

    keys = [
            'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
            'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
            'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
            'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
    ]
    count = 0
    proxy_list = []
    ip_list = []
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    filename = day + '.txt'
    
    start_time = main()
    
    end_time = time.clock()
    print ("Cost time is %f" % (end_time - start_time))
