import scrapy,json,csv,os, requests, urllib, shutil,sys,re
from scrapy import Selector
sys.path.append(os.path.dirname(__file__))
# sys.path.append("C:\\dev")
import functions
class CrawlerSpider(scrapy.Spider):
    name = 'B2bstack'
    start_urls = ['https://www.b2bstack.com.br/categorias']
    def parse(self, response):
        # LINKS=response.xpath('//ul[@class="main-category-list"]/li/ol/a/@href').getall()
        LINKS=response.xpath('//ul[@class="main-category-list"]/li/ol/li/a/@href').getall()
        i=0
        for url in LINKS:
            url="https://www.b2bstack.com.br"+url
            catname=response.xpath('//ul[@class="main-category-list"]/li/ol/li/a/text()').getall()[i]
            yield scrapy.Request(url,callback=self.parse_categories,meta={'pagenum':1,'catname':catname},dont_filter=True)
            i+=1
            # break
    def parse_categories(self, response):
        pagenum=response.meta['pagenum']
        catname=response.meta['catname']
        LINKS=response.xpath('//div[@class="p-head"]/div[@class="info"]/h3/a/@href').getall()
        anpp=len(LINKS)
        for url in LINKS:
            url="https://www.b2bstack.com.br"+url
            # url="https://www.b2bstack.com.br/product/event-manager"#test
            yield scrapy.Request(url,callback=self.parse_product,meta={'catname':catname})
            # break
        if anpp>=10:
            pn=pagenum+1
            if pn==2: 
                url=response.url+"?page=2" 
            else: 
                url=response.url.replace('?page='+str(pagenum),'?page='+str(pn))
            yield scrapy.Request(url,callback=self.parse_categories,meta={'pagenum':pn,'catname':catname},dont_filter=True)
    def parse_product(self, response):
        productdetail={}
        productdetail['url']=response.url
        productdetail['catname']=response.meta['catname']
        productdetail['name']=response.xpath('//h1/text()').get().strip()
        productdetail['developer']=functions.cleanhtml(response.xpath('//p[@class="powered"]').get())
        htmlinfo=response.xpath('//section[@id="info"]').get()
        allcontent=htmlinfo.split('<hr>')
        content = allcontent[0].replace("\n","")
        sel = Selector(text=content)#get by xpath
        pabouts=sel.xpath('//p/text()').getall()
        i=0
        about=""
        for pa in pabouts:
            if i>4:
                about += pa
            i+=1
        productdetail['about']=about
        content=allcontent[1].replace("\n","")
        sel = Selector(text=content)#get by xpath
        pindicado=sel.xpath('//p/text()').getall()
        indicado=""
        for pi in pindicado:
            if pi.strip() != '':
                indicado+=pi
        productdetail['indicado']=indicado
        content=allcontent[3].replace("\n","")
        sel = Selector(text=content)#get by xpath
        try:
            cprice=sel.xpath('//ul/li').getall()
            j=0
            price={}
            for cp in cprice:
                h4=sel.xpath('//ul/li/h4/text()').getall()[j]
                cpc=functions.cleanhtml(cp).replace(h4,"").strip()
                price[h4]=cpc
                j+=1
            price=json.dumps(price, ensure_ascii=False).encode('utf8').decode()
        except:
            price=""
        productdetail['planos_precos']=price
        content=allcontent[4].replace("\n","")
        sel = Selector(text=content)#get by xpath
        mixdetail = sel.xpath('//ul/li').getall()
        Site=""
        Linkedin=""
        Fabricante=""
        Funda=""
        Suporte=""
        Treinamento=""
        Plataforma=""
        for detail in mixdetail:
            sel1=Selector(text=detail)
            if sel1.xpath('//h3/text()').get()=='Site':
                Site=sel1.xpath('//a/@href').get()
            if sel1.xpath('//h3/text()').get()=='Linkedin':
                Linkedin=sel1.xpath('//a/@href').get()
            if sel1.xpath('//h3/text()').get()=='Fabricante':
                Fabricante=functions.cleanhtml(detail).replace('Fabricante',"").strip()
            if sel1.xpath('//h3/text()').get()=='Fundação':
                Funda=functions.cleanhtml(detail).replace('Fundação',"").strip()
            if sel1.xpath('//h3/text()').get()=='Suporte técnico':
                Suporte=functions.cleanhtml(detail).replace('Suporte técnico',"").strip()
            if sel1.xpath('//h3/text()').get()=='Treinamento':
                Treinamento=functions.cleanhtml(detail).replace('Treinamento',"").strip()
            if sel1.xpath('//h3/text()').get()=='Plataforma':
                Plataforma=functions.cleanhtml(detail).replace('Plataforma',"").strip()
        productdetail['site']=Site
        productdetail['linkedin']=Linkedin
        productdetail['fabricante']=Fabricante
        productdetail['fundacao']=Funda
        productdetail['suporte']=Suporte
        productdetail['treinamento']=Treinamento
        productdetail['plataforma']=Plataforma
        # print(productdetail)
        rvurl=response.url+"/avaliacoes?page=1"
        yield scrapy.Request(rvurl,callback=self.parse_reviews,meta={'productdetail':productdetail,'pagervnum':1},dont_filter=True)
    def parse_reviews(self, response):
        productdetail=response.meta['productdetail']
        pagervnum=response.meta['pagervnum']
        url=response.url
        reviews=response.xpath('//div[@class="review"]').getall()
        # print(reviews)
        if len(reviews)>0:
            for rev in reviews:
                content=rev.replace("\n","")
                sel = Selector(text=content)#get by xpath
                review_name=sel.xpath('//p[@class="evaluator "]/text()').get().strip()
                try:
                    review_job=sel.xpath('//p[@class="evaluator "]/span/text()').getall()[0].strip()
                except:
                    review_job=""
                try:
                    review_company=sel.xpath('//p[@class="evaluator "]/span/text()').getall()[1].strip().replace('Em: ','')
                except:
                    review_company=""
                review_recomendacao=sel.xpath('//div[@class="nps"]/strong/text()').get().strip()
                review_facilidade_de_uso=sel.xpath('//div[@class="grades"]/div[@class="grade"]/strong/text()').getall()[0]
                review_suporte_ao_cliente=sel.xpath('//div[@class="grades"]/div[@class="grade"]/strong/text()').getall()[1]
                review_custo_beneficio=sel.xpath('//div[@class="grades"]/div[@class="grade"]/strong/text()').getall()[2]
                review_funcionalidades=sel.xpath('//div[@class="grades"]/div[@class="grade"]/strong/text()').getall()[3]
                try:
                    review_title=sel.xpath('//h3/text()').get().strip()
                except:
                    review_title=""
                review_q1=sel.xpath('//div[@class="answers"]/h4/text()').getall()[0].strip()
                review_q1_answer=sel.xpath('//div[@class="answers"]/p/text()').getall()[0].strip()
                review_q2=sel.xpath('//div[@class="answers"]/h4/text()').getall()[1].strip()
                review_q2_answer=sel.xpath('//div[@class="answers"]/p/text()').getall()[1].strip()
                review_q3=sel.xpath('//div[@class="answers"]/h4/text()').getall()[2].strip()
                review_q3_answer=sel.xpath('//div[@class="answers"]/p/text()').getall()[2].strip()
                review_date=sel.xpath('//div[@class="review-footer"]/p[@class="published"]/text()').get().strip()
                with open('B2bstack.csv', 'a', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([productdetail['url'],productdetail['catname'],productdetail['name'],productdetail['developer'],productdetail['about'],productdetail['indicado'],productdetail['planos_precos'],productdetail['site'],productdetail['linkedin'],productdetail['fabricante'],productdetail['fundacao'],productdetail['suporte'],productdetail['treinamento'],productdetail['plataforma'],review_name,review_job,review_company,review_recomendacao,review_facilidade_de_uso,review_suporte_ao_cliente,review_custo_beneficio,review_funcionalidades,review_title,review_q1,review_q1_answer,review_q2,review_q2_answer,review_q3,review_q3_answer,review_date])
        else:
            with open('B2bstack.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([productdetail['url'],productdetail['catname'],productdetail['name'],productdetail['developer'],productdetail['about'],productdetail['indicado'],productdetail['planos_precos'],productdetail['site'],productdetail['linkedin'],productdetail['fabricante'],productdetail['fundacao'],productdetail['suporte'],productdetail['treinamento'],productdetail['plataforma'],"","","","","","","","","","","","","","","",""])
        if len(reviews)>=10:
            pagenum=pagervnum+1
            url=url.replace('='+str(pagervnum),'='+str(pagenum))
            yield scrapy.Request(url,callback=self.parse_reviews,meta={'productdetail':productdetail,'pagervnum':pagenum},dont_filter=True)