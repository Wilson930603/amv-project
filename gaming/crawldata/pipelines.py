import pymongo
class CrawldataPipeline:
    def open_spider(self, spider):
        spider.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        spider.mydb = spider.myclient["CRAWLER"]
        spider.mycol = spider.mydb[spider.name]
    def close_spider(self, spider):
        spider.myclient.close()
    def process_item(self, item, spider):
        try:
            spider.mycol.insert_one(item)
        except:
            print('\n ------------')
            print(item)
        return item