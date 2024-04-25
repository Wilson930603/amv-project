from scrapy import Spider, Request
from ..utilities import *
from ..items import KitchenrepairItem


class Cfsa(Spider):
    name = "cfsa"
    start_url = "https://cfesa.com/directory/page/{pgno}/?wpbdp_sort=field-1"
    headers = return_headers()

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def start_requests(self):
        
        for pgno in range(1, 41):
            yield Request(
                url=self.start_url.format(pgno=pgno),
                callback=self.main_page,
                headers=self.headers,
            )
            # break

    def main_page(self, response):

        locations = response.xpath('//div[@class="listing-title"]//a')
        for location in locations:
            location_name = location.xpath(".//text()").get()
            location = location.xpath('.//@href').get()
            yield Request(
                url=location,
                callback=self.location_page,
                headers=self.headers,
                meta={"location_name": location_name},
            )

    def location_page(self, response):
        location_name = response.meta.get('location_name')
        city = if_na( response.xpath('//span[text()="City"]/following-sibling::div/text()').get())
        state = if_na( response.xpath('//span[text()="State"]/following-sibling::div/text()').get())
        zipcode = if_na( response.xpath('//span[text()="ZIP Code"]/following-sibling::div/text()').get())
        toll_free_number = if_na( response.xpath('//span[text()="Toll-Free Number"]/following-sibling::div//text()').get())
        business_fax = if_na( response.xpath('//span[text()="Business Fax"]/following-sibling::div//text()').get())
        business_website = if_na( response.xpath('//span[text()="Business Website Address"]/following-sibling::div//text()').get())
        primary_contact = if_na( response.xpath('//span[text()="Primary Contact"]/following-sibling::div//text()').get())
        primary_job_title = if_na( response.xpath('//span[text()="Primary Contact Job Title"]/following-sibling::div//text()').get())
        email = if_na( response.xpath('//span[text()="Primary Contact Email"]/following-sibling::div//text()').get())
        installation_level = if_na( response.xpath('//span[text()="Installation Level"]/following-sibling::div//text()').get()        )
        services_offered = if_na( response.xpath('//span[text()="Services offered"]/following-sibling::div//text()').get())
        year_established = if_na( response.xpath('//span[text()="Year Established"]/following-sibling::div//text()').get())
        member_since = if_na( response.xpath('//span[text()="CFESA Member since"]/following-sibling::div//text()').get())
        member_group = if_na( response.xpath('//span[text()="Member Group"]/following-sibling::div//text()').get())
        region = if_na( response.xpath('//span[text()="CFESA Geographical Region"]/following-sibling::div//text()').get())
        items = KitchenrepairItem()
        items['URL'] = response.url
        items['City'] = city
        items['State'] = state
        items['ZIPCode'] = zipcode
        items['TollFreeNumber'] = toll_free_number
        items['BusinessFax'] = business_fax
        items['BusinessWebsiteAddress'] = business_website
        items['PrimaryContact'] = primary_contact
        items['PrimaryContactJobTitle'] = primary_job_title
        items['PrimaryContactEmail'] = email
        items['InstallationLevel'] = installation_level
        items['Servicesoffered'] = services_offered
        items['YearEstablished'] = year_established
        items['CFESAMembersince'] = member_since
        items['MemberGroup'] = member_group
        items['CFESAGeographicalRegion'] = region
        yield items
