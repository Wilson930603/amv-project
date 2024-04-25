# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import os
class SocialbladePipeline:
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        #input(f'Pipeline: {adapter}')
        if adapter.get('Website') == 'Facebook':
            items ={
                'Brand':[],
                'Website':[],
                'Page_likes':[],
                'Talking_about':[],
                'TotalLikes_monthly':[],
                'TotalTalking_monthly':[],
            }
            items['Brand'].append(adapter.get('Brand'))
            items['Website'].append(adapter.get('Website'))
            items['Page_likes'].append(adapter.get('Page_likes'))
            items['Talking_about'].append(adapter.get('Talking_about'))
            items['TotalLikes_monthly'].append(adapter.get('TotalLikes_monthly'))
            items['TotalTalking_monthly'].append(adapter.get('TotalTalking_monthly'))
            file_name = './datafolder/socialBladeFacebook.csv'
            if not os.path.exists(file_name):
                pd.DataFrame(items).to_csv(file_name,index=False)
            else:
                pd.DataFrame(items).to_csv(file_name,index=False,header=False,mode='a')
        else:
            items={
                'Brand':[],
                'Website':[],
                'Uploads':[],
                'Subcribers':[],
                'VideoViews':[],
                'country':[],
                'ChannelType':[],
                'UserCreated':[],
                'subscriberOverTime':[],
                'videoOverTime':[],
            }

            items['Brand'].append(adapter.get('Brand'))
            items['Website'].append(adapter.get('Website'))
            items['Uploads'].append(adapter.get('Uploads'))
            items['Subcribers'].append(adapter.get('Subcribers'))
            items['VideoViews'].append(adapter.get('VideoViews'))
            items['country'].append(adapter.get('country'))
            items['ChannelType'].append(adapter.get('ChannelType'))
            items['UserCreated'].append(adapter.get('UserCreated'))
            items['subscriberOverTime'].append(adapter.get('subscriberOverTime'))
            items['videoOverTime'].append(adapter.get('videoOverTime'))
            file_name = './datafolder/socialBladeYoutube.csv'
            if not os.path.exists(file_name):
                pd.DataFrame(items).to_csv(file_name,index=False)
            else:
                pd.DataFrame(items).to_csv(file_name,index=False,header=False,mode='a')
        return item
