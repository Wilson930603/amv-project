from scrapy.exporters import CsvItemExporter
import os
from datetime import datetime
class CrawldataPipeline:
    def open_spider(self, spider):
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
        self.exporter.export_item(item)
        return item