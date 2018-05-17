##### HEADERS #####

import scrapy
from scrapy import log

##### DATA STRUCTURES #####

# tableItem:
# {
# 	"company" : <extracted data>,
#	"contact" : <extracted data>,
# 	"country" : <extracted data>
# }
class tableItem(scrapy.Item):
	company = scrapy.Field()
	contact = scrapy.Field()
	country = scrapy.Field()

# itemSpider
class itemSpider(scrapy.Spider):
	name = 'sample' # name of spider
	start_urls = ['https://www.w3schools.com/html/html_tables.asp'] # website url

	def parse(self, response):
		item = tableItem() # generate instance of an item
		rows = response.xpath('//table[@id="customers"]/tr') # get rows from table
		for row in rows[1:]:
			item['company'] = row.xpath('td[1]/text()').extract() # extract from row
			item['contact'] = row.xpath('td[2]/text()').extract() # extract from row
			item['country'] = row.xpath('td[3]/text()').extract() # extract from row
			yield item # return instance of item
