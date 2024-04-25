from scrapy.exporters import CsvItemExporter
import os,json
from datetime import datetime
class CrawldataPipeline:
    def open_spider(self, spider):
        file_log = './log'
        if not os.path.exists(file_log):
            os.mkdir(file_log,0o777)
        # --------------------
        self.file_path_producer = './Data'
        if not os.path.exists(self.file_path_producer):
            os.mkdir(self.file_path_producer,0o777)
        self.file_path_producer+= '/'+spider.name+'.json'
        self.DATASET=[]

    def close_spider(self, spider):
        f=open(self.file_path_producer,'w',encoding='utf-8')
        f.write(json.dumps(self.DATASET))
        f.close()
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
        self.DATASET.append(item)
        return item