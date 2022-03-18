import scrapy
#import json
from scrapy.linkextractors import LinkExtractor



class RealestateScraperItem(scrapy.Item):
	# default_input_processor = MapCompose(unicode.strip)
	# define the fields for your item here like:
	link = scrapy.Field()  #
	gouvernorat = scrapy.Field()
	delegation = scrapy.Field()
	localite = scrapy.Field()
	codeP = scrapy.Field()
	adresse = scrapy.Field()
	superficie_habitable = scrapy.Field()  #
	superficie_terrain = scrapy.Field()  #
	nbpiece = scrapy.Field()  #
	price = scrapy.Field()  #
	anneeConst = scrapy.Field()  #
	description = scrapy.Field()  #
	typeImm = scrapy.Field()  #
	service = scrapy.Field()
	plein_air = scrapy.Field()  #
	chauffage = scrapy.Field()
	salle_de_bain = scrapy.Field()  #
	climatisation = scrapy.Field()
	cuisine = scrapy.Field()
	installations_sportives = scrapy.Field()
	fonds = scrapy.Field()  #
	constructible = scrapy.Field()  #
	dateAnnonce = scrapy.Field()
	tel = scrapy.Field()
	agence = scrapy.Field()
	reference = scrapy.Field()


class MenziliSpider(scrapy.Spider):
	name = 'MenziliSpider'  
	allowed_domains = ["menzili.tn"]
	start_urls = [		
		'https://www.menzili.tn/immo/vente-immobilier-tunisie?l=1&page=1&tri=1'
	]

	def parse(self, response):
		for item in self.scrape(response):
			yield item
		nextpageurl = response.xpath("//html/body/section[2]/div/div/div[2]/div/div/ul[@class='pagination']/li/a[contains(text(),'>')]/@href")
		if nextpageurl is not None:
			path = nextpageurl.extract_first()
			nextpage = response.urljoin(path)
			yield scrapy.Request(nextpage, callback=self.parse)

       
	def scrape(self, response):
		for resource in response.xpath("//html/body/section[2]/div/div/div/div/div/div/div[@class=' listing-actions ']/a[@class='show-info']"): 
			profilepage = response.urljoin(resource.xpath("@href").extract_first())
			request= scrapy.Request(profilepage, callback=self.get_details,meta={"link":profilepage})
			yield request 

	def get_details(self, response):
		item = RealestateScraperItem()
		item['link'] = response.meta['link'] 
		item['typeImm']=response.xpath("/html/body/section[@id='main-product']/div['container']/div[@class='row breadcrumb']/a[2]/span/text()").extract_first()
		item['price'] = response.xpath("//html/body/section[@id='main-product']/div[@class='product-title']/div[@class='container']/div[@class='row']/div[@class='col-md-4 col-xs-12 col-sm-5 product-price']/p/text()").extract_first()
		item['adresse']= response.xpath("//html/body/section[@id='main-product']/div[@class='product-title']/div[@class='container']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-7 product-title-h1']/p/text()").extract_first()
		item['dateAnnonce']= response.xpath("//html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-ref text-center']/div[@class='col-md-4 col-xs-12 col-sm-4']/span/strong/time/text()").extract_first()
		if response.xpath("//html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-4 col-xs-12 col-sm-12 product-right-bar']/div[@class='col-md-12 col-xs-12 col-sm-12 right-bar-userinfo']/div[@class='col-md-12 col-xs-12 col-sm-12 block-1']/div[@class='text-center  ']/p/span[@class='badge']/text()").extract_first()=='PRO':
			item['agence']='agence'
			agence=1
		else :
			item['agence']='particulier'
			agence=0
			
		if agence :
			item['agence']= response.xpath("//html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-4 col-xs-12 col-sm-12 product-right-bar']/div[@class='col-md-12 col-xs-12 col-sm-12 right-bar-userinfo']/div[@class='col-md-12 col-xs-12 col-sm-12 block-1']/div[@class='text-center  ']/p/a/strong/text()").extract_first()
		else:
			item['agence']= response.xpath("//html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-4 col-xs-12 col-sm-12 product-right-bar']/div[@class='col-md-12 col-xs-12 col-sm-12 right-bar-userinfo']/div[@class='col-md-12 col-xs-12 col-sm-12 block-1']/div[@class='text-center  ']/p/a/strong/text()").extract_first()
		item['tel']= response.xpath("/html/body/section[1]/div[3]/div/div[@class='col-md-4 col-xs-12 col-sm-12 product-right-bar']/div[@class='col-md-12 col-xs-12 col-sm-12 right-bar-userinfo']/div[@class='col-md-12 col-xs-12 col-sm-12 block-2  ']/span[@class=' btn col-md-12 col-xs-12 col-sm-12']/text()").extract()
		nb=len(response.xpath("/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div").extract())
		for i in range(1,nb):		
			exp="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/span/text()"
			if response.xpath(exp).extract_first() == 'Chambres : ' :
				exp2="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/strong/text()"
				item['nbpiece']=response.xpath(exp2).extract_first()
			elif(response.xpath(exp).extract_first() =='Salle de bain : '):
				exp2="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/strong/text()"
				item['salle_de_bain']=response.xpath(exp2).extract_first()
			elif(' (Totale) ' in response.xpath(exp).extract_first() ):
				exp2="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/strong/text()"
				item['nbpiece']=response.xpath(exp2).extract_first()
			elif(response.xpath(exp).extract_first() =='Surf habitable : '):
				exp2="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/strong/text()"
				item['superficie_habitable']=response.xpath(exp2).extract_first()
			elif(response.xpath(exp).extract_first() =='Surf terrain : '):
				exp2="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div["+ str(i)+"]/strong/text()"
				item['superficie_terrain']=response.xpath(exp2).extract_first()
		exp="/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-detail ']/div/div[@class='col-md-12 col-xs-12 col-sm-12 block-over']/span"
		numb=len(response.xpath(exp).extract())
		desc=response.xpath("/html/body/section[@id='main-product']/div[@class='container main-product']/div[@class='row']/div[@class='col-md-8 col-xs-12 col-sm-12 product-content']/div[@class='col-md-12 col-xs-12 col-sm-12 block-descr']/p/text()").extract()
		for i in range (1,numb):
			exp2=exp+"["+str(i)+"]/strong/text()"
			rep=response.xpath(exp2).extract()
			desc.append(rep)
		item['description']= desc			
		yield item

