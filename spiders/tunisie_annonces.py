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



class TunisieAnnonVentesSpider(scrapy.Spider):
    #i=0
    name = 'TunisieAnnonVentesSpider'
    start_urls = ["http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_cod_rub=101&rech_cod_typ=10102&rech_cod_sou_typ=&rech_cod_pay=TN&rech_cod_reg=&rech_cod_vil=&rech_cod_loc=&rech_prix_min=&rech_prix_max=&rech_surf_min=&rech_surf_max=&rech_age=&rech_photo=&rech_typ_cli=&rech_order_by=31&rech_page_num=123"]
    

    
    def parse(self, response):
            # The main method of the spider. It scrapes the URL(s) specified in the
            # 'start_url' argument above. The content of the scraped URL is passed on
            # as the 'response' object.

        for href in response.xpath("//a[contains(@href,'ann=')]/@href"):
            print("*******************INSIDE ITEMS LOOP**********************")
            item = RealestateScraperItem() # Creating a new Item object
            url = response.urljoin(href.extract())
            item['link']= url
            request = scrapy.Request(url, callback=self.get_details)
            request.meta['item'] = item
            yield request
        
        next_page=""
        current_page=next_page
        next_page = response.xpath("//a[img/@src ='/images/n_next.gif']/@href").extract_first()
        if (next_page and current_page!=next_page):
            print("*******************MOVING TO NEXT PAGE**********************")
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse, dont_filter = True)

            
    def get_details(self, response):

        print("*******************SCRAPPING ITEM**********************")
        # A scraper designed to operate on one of the profile pages
        item = response.meta['item'] #Get the item we passed from scrape()
        #item = RealestateScraperItem()
       
        #SCRAPING REFERENCE
        item['reference']= None
        if response.xpath("//*[@class='da_entete']/td/text()").extract_first() is not None:
            start = '['
            end = ']'
            ref=response.xpath("//*[@class='da_entete']/td/text()").extract_first()
            ref=ref[ref.find(start)+len(start):ref.rfind(end)]     
            item['reference']= ''.join(c for c in ref if c.isdigit())

        #SCRAPING DATE DEP
        item['dateAnnonce']="NA"
        if response.xpath("//*[text()[contains(.,'Insérée le')]]/following-sibling::td/text()").extract_first() is not None:
            item['dateAnnonce']=(response.xpath("//*[text()[contains(.,'Insérée le')]]/following-sibling::td/text()").extract_first())

        #SCRAPING PRICE
        item['price']=None
        if response.xpath("//*[text()[contains(.,'Prix')]]/following-sibling::td/text()").extract_first()  is not None:
            item['price'] =(response.xpath("//*[text()[contains(.,'Prix')]]/following-sibling::td/text()").extract_first() )

        #SCRAPING SUPERFICIE HABITABLE
        item['superficie_habitable']=None
        if response.xpath("//*[text()[contains(.,'Surface')]]/following-sibling::td/text()").extract_first()  is not None:
            item['superficie_habitable']=(response.xpath("//*[text()[contains(.,'Surface')]]/following-sibling::td/text()").extract_first() )

        #SCRAPING SUPERFICIE HABITABLE
        item['superficie_terrain']=None
  
        #SCRAPING CODE POSTAL 
        item['codeP']=None

        #SCRAPING GOUVERNERAT 
        item['gouvernorat']=None
        if response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[2]").extract_first() is not None:
            item['gouvernorat']=(response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[2]/text()").extract_first())
       
        #SCRAPING DELEGATION 
        item['delegation']=None
        if response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[3]").extract_first() is not None:
            item['delegation']=(response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[3]/text()").extract_first())

        #SCRAPING LOCALITE 
        item['localite']=None
        if response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[4]").extract_first() is not None:
            item['localite']=(response.xpath("//*[text()[contains(.,'Localisation')]]/following-sibling::td/a[4]/text()").extract_first())

        #SCRAPING ADRESSE 
        item['adresse']=None
        if response.xpath("//*[text()[contains(.,'Adresse')]]/following-sibling::td/text()").extract_first() is not None:
            item['adresse']=(response.xpath("//*[text()[contains(.,'Adresse')]]/following-sibling::td/text()").extract_first())
        
        #SCRAPING ANNE DE CONSTRUCTION 
        item['anneeConst']=None

        #SCRAPING NB PIECES 
        item['nbpiece']=None

        #SCRAPING TYPEIMM 
        item['typeImm']=None
        if response.xpath("//*[text()[contains(.,'Catégorie')]]/following-sibling::td/a[3]/text()").extract_first() is not None:
            item['typeImm']=(response.xpath("//*[text()[contains(.,'Catégorie')]]/following-sibling::td/a[3]/text()").extract_first())

        #SCRAPING FONDS
        item['fonds']=None

        #SCRAPING PLEIN AIR
        item['plein_air']=None

        #SCRAPING SALLE DE BAIN
        item['salle_de_bain']=None
     
        #SCRAPING CONSTRUCTIBLE
        item['constructible']=None

        #SCRAPING SERVICE 
        item['service']=None

        #SCRAPING CHAUFFAGE 
        item['chauffage']=None

        #SCRAPING CLIMATISATION 
        item['climatisation']=None

        #SCRAPING CUISINE 
        item['cuisine']=None

        #SCRAPING INST SPORT 
        item['installations_sportives']=None

        #SCRAPING TELEPHONE 
        item['tel']=None
        if response.xpath("//span[@class='da_contact_value']/text()").extract() is not None:
            item['tel']=response.xpath("//span[@class='da_contact_value']/text()").extract()

        #SCRAPING AGENCE 
        item['agence']=None
        
        #SCRAPING DESCRIPTION
        item['description']=None
        fulldesc=response.xpath("//td[text()[contains(.,'Texte')]]/following-sibling::td/text()").extract()
        if fulldesc is not None:
            item['description']= ""
            for el in fulldesc:
                item['description']+=(" \n"+str(el))

        
        yield item #Return the new phonenumber'd item back to scrape
