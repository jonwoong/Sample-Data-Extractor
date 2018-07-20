# Author: Jonathan Woong

import scrapy

class tableItem(scrapy.Item): # insert column fields here	

class itemSpider(scrapy.Spider):
	name = '$NAME'
	start_urls = ['$URL']

	def parse(self,response):
		item = tableItem()
		rows = response.xpath('//table[@$ATTRIBUTE="$VALUE"]/tr')
		for row in rows[1:]: # insert row extraction here
		
			yield item