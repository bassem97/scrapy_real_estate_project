import scrapy
from scrapy.spiders import CrawlSpider,Rule
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



class TecnoSpider(scrapy.Spider):
	name= 'tecnoSpider'
	start_urls = ['https://www.tecnocasa.tn/vendre/immeubles/nord-est-ne/cap-bon.html',
				  'https://www.tecnocasa.tn/vendre/immeubles/nord-est-ne/grand-tunis.html',
				  'https://www.tecnocasa.tn/vendre/immeubles/centre-est-ce/mahdia.html'
		,'https://www.tecnocasa.tn/vendre/immeubles/centre-est-ce/monastir.html',
				  'https://www.tecnocasa.tn/vendre/immeubles/centre-est-ce/sousse.html']
	def parse(self, response):
		for resource in response.xpath("//body/div[@id='sb-site']/div[@class='boxed side-collapse-container ']/div[@class='content']/div[@class='container immobiliListaAnnunci']/div[@class='row']/div[@class='col-md-12 col-lg-12 padding0']/div/div[@class='row immobiliListaAnnuncio']/a[@class='immobileLink']"): 
			item = RealestateScraperItem() # Creating a new Item object
			profilepage = response.urljoin(resource.xpath("@href").extract_first())
			item['link'] = profilepage
			request= scrapy.Request(profilepage, callback=self.get_details)
			request.meta['item'] = item 
			yield request
		
		nextpageurl=None
		nextpageurl = response.xpath("//html/body/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/nav/div/div/div[1]/ul[@class='pagination']/li/a[contains(text(),'>')]/@href")
		if nextpageurl is not None:
			path = nextpageurl.extract_first()
			nextpage = response.urljoin(path)
			yield scrapy.Request(nextpage, callback=self.parse, dont_filter = True)

	def get_details(self, response):
		# A scraper designed to operate on one of the profile pages
		item = response.meta['item'] #Get the item we passed from scrape()
		
		item['reference']= None
		if response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[3]/h1/span/text()").extract_first() is not None:
			ref=response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[3]/h1/span/text()").extract_first()
			ref=ref[6:]     
			item['reference']=''.join(c for c in ref if c.isdigit())
		
		item['price']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Prix')]]/following-sibling::text()").extract() is not None:
			item['price'] = response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Prix')]]/following-sibling::text()").extract()
		
		item['superficie_terrain']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Superficie')]]/following-sibling::text()").extract() is not None:
			item['superficie_terrain']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Superficie')]]/following-sibling::text()").extract()
		
		item['codeP']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Code postal')]]/following-sibling::text()").extract() is not None:
			item['codeP']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Code postal')]]/following-sibling::text()").extract()
		
		item['delegation']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Ville')]]/following-sibling::text()").extract() is not None:
			item['delegation']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Ville')]]/following-sibling::text()").extract()
		

		item['gouvernorat']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'gion')]]/following-sibling::text()").extract() is not None:
			item['gouvernorat']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'gion')]]/following-sibling::text()").extract()
		
		item['anneeConst']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'de construction')]]/following-sibling::text()").extract() is not None:
			item['anneeConst']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'de construction')]]/following-sibling::text()").extract()
		
		item['nbpiece']=None
		if response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Pi')]]/following-sibling::text()").extract() is not None:
			item['nbpiece']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Pi')]]/following-sibling::text()").extract()
		
		item['typeImm']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/*[text()[contains(.,'Typologie')]]/following-sibling::text()").extract()
		
		
		if response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/text()[contains(.,'constructible')]") is not None:
			item['constructible']=response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/text()[contains(.,'constructible')]").extract()
		elif response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/text()[contains(.,'agricole')]") is not None:
			item['constructible']=response.xpath("/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[6]/div/div/text()[contains(.,'constructible')]").extract()
		else: 
			item['constructible']=None
		item['description']=response.xpath("//html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[5]/p/text()").extract_first()
			
		for i in range(1,9):
			exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/strong/text()"
			if len(response.xpath(exp).extract())>0:
				if(response.xpath(exp).extract()[0] =='Service'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['service']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Appareils de plein air'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['plein_air']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Chauffage'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['chauffage']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Salle de bain'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['salle_de_bain']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Climatisation'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['climatisation']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Cuisine'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['cuisine']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Installations sportives'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['installations_sportives']=response.xpath(exp).extract()
				elif(response.xpath(exp).extract()[0] =='Les envois de fonds'):
					exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
					item['fonds']=response.xpath(exp).extract()
				#elif(response.xpath(exp).extract()[0] =='Local'):
				#	exp="/html/body/div[1]/div/div[3]/div/div[2]/div/div/div[3]/div[7]/div[1]/div/div["+str(i)+"]/ul/li/text()"
				#	item['Local']=response.xpath(exp).extract()
		yield item #Return the new phonenumber'd item back to scrape
