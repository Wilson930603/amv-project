from scrapy.exporters import CsvItemExporter
import os
from datetime import datetime
from crawldata.functions import *

class CrawldataPipeline:
    def open_spider(self, spider):
        self.DATASET={}
        file_log = './log'
        if not os.path.exists(file_log):
            os.mkdir(file_log,0o777)
        # --------------------
        file_path_producer = './Data'
        if not os.path.exists(file_path_producer):
            os.mkdir(file_path_producer,0o777)
        file_path_producer+= '/'+spider.name+'.csv'
        self.file = open(file_path_producer, 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8-sig')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        item_dt={'TRUE_DOMAIN':'','RESPONSIVE':'','HEADER':'','NAV':'','LINK_IN':0,'LINK_OUT':0,'EMAIL':0,'SOCIAL':0,'H1':0,'H2':0,'H3':0,'H4':0,'H5':0,'H6':0,'Status':'Can not crawl'}
        for URL in spider.URLS:
            row=str(URL).split('~')
            if not str(row[1]).startswith('http'):
                row[1]='http://'+row[1]
            item={'ID':row[0],'URL':row[1]}
            KEY=key_MD5(item['ID']+item['URL'])
            if KEY in self.DATASET:
                self.exporter.export_item(self.DATASET[KEY])
            else:
                item.update(item_dt)
                self.exporter.export_item(item)
        self.exporter.finish_exporting()
        self.file.close()
        log_file='./log/'+spider.name+'_'+spider.DATE_CRAWL+'.log'
        SUMMARY=spider.crawler.stats.get_stats()
        if os.path.exists(log_file):
            f=open(log_file,'a',encoding='utf-8')
            f.write('\n============================')
            for k,v in SUMMARY.items():
                f.write('\n'+str(k)+': '+str(v))
            f.close()
        else:
            for k,v in SUMMARY.items():
                print(str(k),': ',str(v))
    def process_item(self, item, spider):
        KEY=key_MD5(item['ID']+item['URL'])
        if not KEY in self.DATASET:
            self.DATASET[KEY]=item
        return item