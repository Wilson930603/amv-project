from scrapy import Spider,Request
from ..items import NetaportaItem
import re
class Netaporta(Spider):
    name = 'netaporta'
    base_url = 'https://www.net-a-porter.com'
    start_url = 'https://www.net-a-porter.com/en-us/shop/azdesigners'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        # 'cookie': '_hjFirstSeen=1; _hjIncludedInSessionSample_2550801=1; _hjSession_2550801=eyJpZCI6IjY2MTFjOGRhLTMyMDQtNDdmYi1hMTMxLTg2Zjk5YTBiYmE4ZSIsImNyZWF0ZWQiOjE2Nzc5Nzk1ODY5NTQsImluU2FtcGxlIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; form_key=EgISZYkagj1xedJT; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-banners-cache-storage=%7B%7D; _gcl_au=1.1.25486092.1677979591; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; _gid=GA1.2.836919085.1677979593; _hjSessionUser_2550801=eyJpZCI6IjBmZGEwN2YzLWE4ZjMtNTZjNi05MmUyLTdmYjY1NmEyMDI4MCIsImNyZWF0ZWQiOjE2Nzc5Nzk1ODY5NDUsImV4aXN0aW5nIjp0cnVlfQ==; mg_last_logged_email=Mandy%20Akers; mg_last_email=vendors%40laylagrayce.com; _hjIncludedInPageviewSample=1; PHPSESSID=3322c140ecf3fb20f70162f07f23d2d4; dataservices_customer_id=%22138894%22; dataservices_customer_group=%7B%22customerGroupCode%22%3A%22887309d048beef83ad3eabf2a79a64a389ab1c9f%22%7D; dataservices_cart_id=%221974770%22; private_content_version=2ddd53cd86d1372d7d7df6bd167e651d; X-Magento-Vary=a1cf4e94fb335b68ab94a833d9d1dfb6b62adfce; form_key=EgISZYkagj1xedJT; mage-cache-sessid=true; _ga_DGG2W3LJM2=GS1.1.1677979592.1.1.1677980995.0.0.0; _ga=GA1.1.651922743.1677979592; authentication_flag=false; section_data_ids=%7B%22customer%22%3A1677980997%2C%22compare-products%22%3A1677980997%2C%22last-ordered-items%22%3A1677980997%2C%22requisition%22%3A1677980997%2C%22cart%22%3A1677980997%2C%22directory-data%22%3A1677980997%2C%22captcha%22%3A1677980997%2C%22wishlist%22%3A1677980997%2C%22company%22%3A1677980997%2C%22company_authorization%22%3A1677980997%2C%22negotiable_quote%22%3A1677980997%2C%22instant-purchase%22%3A1677980997%2C%22loggedAsCustomer%22%3A1677980997%2C%22multiplewishlist%22%3A1677980997%2C%22purchase_order%22%3A1677980997%2C%22persistent%22%3A1677980997%2C%22review%22%3A1677980997%2C%22recently_viewed_product%22%3A1677980997%2C%22recently_compared_product%22%3A1677980997%2C%22product_data_storage%22%3A1677980997%2C%22paypal-billing-agreement%22%3A1677980997%7D',
        "referer": "https://www.pigeonandpoodle.com/customer/account/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def start_requests(self):
        yield Request(
            url= self.start_url,
            headers=self.headers,
            callback=self.main_brands,
        )

        pass
    def main_brands(self,response):
        brands = response.xpath('//div[@class="DesignerList0__designerListing"]//a')
        for brand in brands:
            coming_soon = brand.xpath('.//following-sibling::p/text()').get()
            if coming_soon != None:
                if coming_soon == 'COMING SOON':
                    continue
                
            else:
                coming_soon ='N/A'
            brand_name = brand.xpath('.//text()').get().strip()
            brand_link = self.base_url + brand.xpath('.//@href').get()
            yield Request(
                    url= brand_link,
                    callback=self.brand_products,
                    headers=self.headers,
                    meta={"brand_name":brand_name}
                )
    def brand_products(self,response):
        meta = response.meta
        pagination = meta.get('pagination',True)
        brand_name = meta.get('brand_name')
        total_brand_products = response.xpath('//span[@class="ProductListingPage52__totalProducts"]/text()').get()
        total_brand_products = re.findall(r'\d+',total_brand_products)[0]
        brand_products_links = [self.base_url + url for url in response.xpath('//a[div[@class="ProductItem24 ProductList52__productItem"]]/@href').extract()]
        if pagination:
            total_pages = response.xpath('//span[@class="Pagination7__currentPage"]/text()').get()
            if total_pages != None:
                total_pages = int(total_pages.split('of')[-1].strip())
            else:
                total_pages = 0
            for num in range(2,total_pages+1):
                yield Request(
                    url = response.url+f'?pageNumber={num}',
                    callback=self.brand_products,
                    headers=self.headers,
                    meta = {
                    "brand_name":brand_name,
                    "pagination":False,
                    }
                )
        for product_link in brand_products_links:
            yield Request(
                url = product_link,
                callback=self.information,
                headers=self.headers,
                meta={
                'brand_name':brand_name,
                'total_brand_products':total_brand_products,
                },
                dont_filter=True
            )
    def information(self,response):
        meta = response.meta
        brand_name = meta.get('brand_name')
        total_band_products = meta.get('total_brand_products')
        cats = [r.title() for r in response.xpath('//div[@class="ShopMore86__links"]')[0].xpath('.//a/text()').extract()]
        brand_on_page = response.xpath('//div[@class="ProductDetails86__basicInfo"]//h1/meta[@itemprop="name"]/@content').get()
        if brand_name.title().strip() in cats:
            cats.remove(brand_name.title().strip())
        elif brand_on_page.title().strip() in cats:
            cats.remove(brand_on_page.title().strip())

        product_name = response.xpath('//p[@class="ProductInformation86__name"]/text()').get()
        product_price = response.xpath('//span[@itemprop="price"]/@content').get()
        categories = {num:cat for num,cat in enumerate(cats)}
        attributes = ['ProductCategory','ProductSubCategory','ProductSubsubCategory']
        items = NetaportaItem()
        items['ProductURL'] = response.url
        items['MainCategory'] = categories.get(0)
        items['Brand'] = brand_name
        items['BrandTotalProducts'] = total_band_products
        items['ProductName'] = product_name
        items['ProductPrice'] =product_price
        for num in range(3):
            items[attributes[num]] = categories.get(num,'N/A')

        yield items