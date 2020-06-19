import requests, sys, time, lockfile
import threading, queue
from requests.packages import urllib3
urllib3.disable_warnings()

#proxies={'http':'http://27.155.84.233:8081'}
class proxy_check(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        global filename, count, pass_count
        while  not self._queue.empty():
            pass_count += 1
            if pass_count % 100 == 0:
                print(pass_count)
            proxy = self._queue.get()
            proxies = {'http':'http://'+proxy}

            burp0_headers = {"Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Accept-Language": "en", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36", "Connection": "close"}
            try:
                r = requests.get(url='http://2020.ip138.com:80/',proxies=proxies,timeout=7, headers=burp0_headers)

            except Exception as e:
                pass
            else:
##                if r.status_code == 200:
##                    print("url='http://2020.ip138.com:80/',proxies="+str(proxies)+",timeout=5, headers="+str(burp0_headers))
                if '您的iP地址是：[' in r.text:
                    if r.text.split('<title>您的IP地址是：')[1].split('</title>')[0] == proxy.split(':')[0]:
                        count += 1
                        print ('---------[success] '+ proxy + '  共已采集 ' + str(count) + ' 个代理---')
                        
                        with open('verify_'+filename,'a',encoding='utf-8') as f:
                            file_lock = lockfile.MkdirFileLock('已验证_'+filename)    
                            while(1):
                                try:
                                    file_lock.acquire()
                                except:
                                    time.sleep(0.1)
                                else:
                                    break
                            f.write('<Proxy CN 0.00s [] ' + proxy + '>\n')
                            file_lock.release()

def main():
    threads = []
    Queue = queue.Queue()
    proxys = []
    
    with open(filename,'r',encoding='utf-8') as f:
        lists = f.readlines()

    for i in lists:
        if '    "proxy": "' in i:
            proxys.append(i.split('    "proxy": "')[1].split('"')[0])
        if '<Proxy US 0.00s [] ' in i:
            proxys.append(i.split('<Proxy US 0.00s [] ')[1].split('>')[0])
    print('待测试：'+str(len(proxys)))

    start_time = time.clock()
    
    for i in proxys:
        Queue.put(i)
        
    for i in range(threads_count):
        threads.append(proxy_check(Queue))	
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    return start_time

if __name__ == '__main__':
    threads_count = 200
    filename = 'proxy'
    count = 0
    pass_count = 0
    
    start_time = main()
    
    end_time = time.clock()
    print ("Cost time is %f" % (end_time - start_time))

