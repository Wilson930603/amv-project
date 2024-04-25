from scrapy.exporters import CsvItemExporter
import os
class CrawldataPipeline:
    def open_spider(self, spider):
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
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item