import pymongo
class CrawldataPipeline:
    def open_spider(self, spider):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["CRAWLER"]
        self.mycol = self.mydb[spider.name]
    def close_spider(self, spider):
        self.myclient.close()
    def process_item(self, item, spider):
        try:
            self.mycol.insert_one(item)
        except:
            print('Existed !!!')
        return item