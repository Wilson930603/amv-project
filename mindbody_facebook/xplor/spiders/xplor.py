import scrapy,json,csv,os, requests, urllib, shutil,sys,re
from scrapy import Selector
sys.path.append(os.path.dirname(__file__))
# sys.path.append("C:\\dev")
import functions
class CrawlerSpider(scrapy.Spider):
    name = 'xplor'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    def start_requests(self):
        with open("ok.txt") as file:
            urls = file.read()
        lstok = urls.strip().split("\n")
        with open("nok.txt") as file:
            urls = file.read()
        lstnok = urls.strip().split("\n")
        with open("full.txt") as file:
            urls = file.read()
        lsturls = urls.split("\n")
        for url in lsturls:
            # if len(url.split('://m.'))>1:
            if url not in lstok and url.strip()!='':
                urlok=url.replace('https://m.','https://')
                urlok=urlok.split("/photos/")[0]
                urlok=urlok.split("/about/")[0]
                urlok=urlok.split("/events/")[0]
                chklg=urlok.split("login/?next=")
                if len(chklg) > 1:
                    urlok=chklg[1].replace('%3A',':').replace('%2F','/')
                yield scrapy.FormRequest(urlok,callback=self.gethtml, method='GET', headers=self.headers,cookies='', formdata='',meta={'surl':url,'lstnok':lstnok},dont_filter=True)
    def gethtml(self,response):
        if response.status == 200:
            lstnok=response.meta['lstnok']
            fburl=response.meta['surl']
            # print(fburl)
            if len(fburl.split("login/?next=")) == 1: 
                chuoi0=""
                chuoi1=""
                tmp=response.text.split("u0040")
                for i in tmp:
                    lastvt=i.rfind('"text":"')
                    if (lastvt!=-1):
                        chuoicon=i[lastvt:]
                        if len(chuoicon)<40  and len(chuoicon.strip().split(' '))==1:
                            chuoi=chuoicon.replace('"text":"','').replace("\\","")
                            if chuoi.strip() != '': chuoi0 = chuoi
                            # print(chuoicon+"\n")
                            cid =  tmp.index(i)
                            nitem = tmp[cid+1]
                            j=nitem.split('"}}')
                            # print(nitem)
                            if len(j)>1 and len(j[0])<40:
                                chuoi1=j[0].strip()
                                # print(j[0].strip()+"\n")
                            if chuoi1=="" and chuoi0.strip() != "":
                                k=nitem.split('","')
                                if len(k)>1 and len(k[0])<40:
                                    chuoi1=k[0].strip()
                                    break
                print(chuoi0+"@"+chuoi1)
                if chuoi0 != "" and chuoi1 != "":
                    email=chuoi0+"@"+chuoi1
                    open("ok.txt",'a',encoding='utf-8').write(fburl+"\n")
                    with open('kq.csv', 'a', newline='', encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([fburl, email])
                else:
                    if fburl not in lstnok:
                        open("nok.txt",'a',encoding='utf-8').write(fburl+"\n")
        else:
            rurl=response.url
            open("rurl.txt",'a',encoding='utf-8').write(rurl+"\n")