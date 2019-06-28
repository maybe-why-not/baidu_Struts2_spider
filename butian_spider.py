import requests,re,json,time
 
headers = {'Host':'www.butian.net',
'Connection':'close',
'Upgrade-Insecure-Requests':'1',
'DNT':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer':'https://www.butian.net/Company/61798',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cookie':'__guid=66782632.1256986472102007600.1557388624680.8123; btlc_ab7a660c7e054d9e446e06f4571ebe41=e0d3fc717e5a6e8883c1a99033c81f64aa1dda8ec7c50b2f0234dbc765f908b5; PHPSESSID=e6efr3lrikba8r1auid98i1u35; __DC_sid=66782632.1996981823297722000.1558628834988.902; __q__=1558629997287; __DC_monitor_count=20; __DC_gid=66782632.36869833.1557388624810.1558630004451.140'
}
url = 'https://www.butian.net/Reward/pub'
 
for page in range(167,175): #前三页
    html = requests.post(url, headers = headers, data={"s": "1", "p": page, "token": ''}).content
    jsCont = json.loads(html.decode())
    jsData = jsCont['data']
    for i in jsData['list']:
        linkaddr = 'https://www.butian.net/Loo/submit?cid=' + i['company_id']
        print(linkaddr)
        shtml = requests.get(linkaddr,headers = headers).content
        #正则模版<input class="input-xlarge" type="text" name="host" placeholder="请输入厂商域名" value="www.grgtest.com" />
        company_url = re.findall('<input class="input-xlarge" type="text" name="host" placeholder="请输入厂商域名" value="(.*)" />',shtml.decode())
        time.sleep(0.5)  # 控制爬取速度
        print(company_url[0])
        com_url = company_url[0]
        with open('butian_company_url.txt','a') as f:
            f.write(com_url + ' ' + linkaddr + '\n')
