import scrapy
from scrapy.spiders import CrawlSpider, Rule
# import json
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


class TunisieImmobSpider(scrapy.Spider):
    name = 'TunisieImmobSpider'
    start_urls = [
        "https://www.tunisieimmob.net/advanced-search/?filter_search_action%5B0%5D=vente&filter_search_type%5B0%5D&advanced_city&submit=RECHERCHE+AVANCEE"]
    # start_urls = ["https://www.tunisieimmob.net/advanced-search/page/110/?filter_search_action%5B0%5D=vente&filter_search_type%5B0%5D&advanced_city&submit=RECHERCHE%20AVANCEE"]
    # rules = ( Rule(LinkExtractor(allow=(),restrict_xpaths=("//*[@id='all_wrapper']//li[@class='roundright']/a",))
    #            , callback='scrapee'
    #            ),
    # Rule(LinkExtractor(restrict_xpaths=("//*[@id='listing_ajax_container']/div/div/h4/a",))
    #    , callback='get_details'),

    # Rule(LinkExtractor(allow='.+/page/\d+$')
    #     , callback='scrape')
    #            )
    next_page = "filler"

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.
        # for item in self.scrape(response):
        #    yield item

        # nextpageurl = response.xpath("//*[@id='all_wrapper']//li[@class='roundright']/a/@href").extract_first()
        # nextpage = response.urljoin(nextpageurl)
        # if nextpage is not None:
        # path = nextpageurl.extract_first()
        #    print("********************WENT OT NEXT PAGE**********************"+nextpage)
        #    yield scrapy.Request(nextpage, callback=self.parse)
        # else:
        #    print("********************NO NEXT PAGE FOUND*********************")

        for href in response.xpath("//*[@id='listing_ajax_container']/div/div/h4/a/@href"):
            print("*******************INSIDE ITEMS LOOP**********************")
            item = RealestateScraperItem()  # Creating a new Item object
            url = response.urljoin(href.extract())
            item['link'] = url
            request = scrapy.Request(url, callback=self.get_details)
            request.meta['item'] = item
            yield request

        current_page = self.next_page
        print("Current page :" + current_page)
        next_page = response.xpath("//*[@id='all_wrapper']//li[@class='roundright']/a/@href").extract_first()
        self.next_page = next_page
        if (next_page and current_page != self.next_page):
            print("*******************MOVING TO NEXT PAGE**********************")
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse, dont_filter=True)
        else:
            print("DO NOTHIN")

    # def scrape(self, response):
    #    for resource in response.xpath("//*[@id='listing_ajax_container']/div/div/h4/a"): 
    #        item = RealestateScraperItem() # Creating a new Item object
    #        profilepage = response.urljoin(resource.xpath("@href").extract_first())
    #        item['link'] = profilepage
    #        request= scrapy.Request(profilepage, callback=self.get_details)
    #        request.meta['item'] = item 
    #        yield request

    def get_details(self, response):

        print("*******************SCRAPPING ITEM**********************")
        # A scraper designed to operate on one of the profile pages
        item = response.meta['item']  # Get the item we passed from scrape()
        # item = RealestateScraperItem()

        # SCRAPING REFERENCE
        item['reference'] = None
        if response.xpath("//*[@id='propertyid_display']/text()").extract_first() is not None:
            item['reference'] = response.xpath("//*[@id='propertyid_display']/text()").extract_first()

        # SCRAPING DATE ANN
        item['dateAnnonce'] = "NA"
        if response.xpath("//*[@class='prop_social']/text()").extract_first() is not None:
            item['dateAnnonce'] = (response.xpath("//*[@class='prop_social']/text()").extract_first())

        # SCRAPING PRICE
        item['price'] = None
        if response.xpath(
                "//*[@id='all_wrapper']//span[@class='price_area']/span[@class='price_label price_label_before']/following-sibling::text()").extract_first() is not None:
            item['price'] = (response.xpath(
                "//*[@id='all_wrapper']//span[@class='price_area']/span[@class='price_label price_label_before']/following-sibling::text()").extract_first())

        # SCRAPING SUPERFECIE HABITABLE
        item['superficie_habitable'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div/div/*[text()[contains(.,'Superficie habitable:')]]/following-sibling::text()").extract_first() is not None:
            item['superficie_habitable'] = (response.xpath(
                "//*[@id='collapseOne']/div/div/*[text()[contains(.,'Superficie habitable:')]]/following-sibling::text()").extract_first())

        # SCRAPING SUPERFECIE TERRAIN
        item['superficie_terrain'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div/div/*[text()[contains(.,'Superficie terrain:')]]/following-sibling::text()").extract_first() is not None:
            item['superficie_terrain'] = (response.xpath(
                "//*[@id='collapseOne']/div/div/*[text()[contains(.,'Superficie terrain:')]]/following-sibling::text()").extract_first())

        # SCRAPING CODE POSTAL
        item['codeP'] = None
        if response.xpath(
                "//*[@id='collapseTwo']/div//*[text()[contains(.,'Code postal:')]]/following-sibling::text()").extract_first() is not None:
            item['codeP'] = (response.xpath(
                "//*[@id='collapseTwo']/div//*[text()[contains(.,'Code postal:')]]/following-sibling::text()").extract_first())

        # SCRAPING GOUVERNERAT
        item['gouvernorat'] = None
        if response.xpath(
                "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Gouvernorat:')]]/a/text()").extract_first() is not None:
            item['gouvernorat'] = (response.xpath(
                "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Gouvernorat:')]]/a/text()").extract_first())

        # SCRAPING DELEGATION
        item['delegation'] = None

        # SCRAPING LOCALITE
        item['localite'] = None

        # SCRAPING ADRESSE
        item['adresse'] = None
        if response.xpath(
                "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Adresse:')]]/text()").extract_first() is not None:
            item['adresse'] = (response.xpath(
                "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Adresse:')]]/text()").extract_first())
            if response.xpath(
                    "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Ville:')]]/a/text()").extract_first() is not None:
                item['adresse'] += "/ Ville : " + response.xpath(
                    "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Ville:')]]/a/text()").extract_first()
            if response.xpath(
                    "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Région:')]]/a/text()").extract_first() is not None:
                item['adresse'] += "/ Région : " + response.xpath(
                    "//*[@id='collapseTwo']/div/div[strong[contains(text(),'Région:')]]/a/text()").extract_first()

        # SCRAPING ANNE DE CONSTRUCTION
        item['anneeConst'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Année De Construction:')]]/following-sibling::text()").extract_first() is not None:
            item['anneeConst'] = (response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Année De Construction:')]]/following-sibling::text()").extract_first())

        # SCRAPING NB PIECES
        item['nbpiece'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Pièces:')]]/following-sibling::text()").extract_first() is not None:
            item['nbpiece'] = (response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Pièces:')]]/following-sibling::text()").extract_first())

        # SCRAPING TYPE IMM
        item['typeImm'] = None
        if response.xpath(
                "//*[@id='all_wrapper']//div[@class='property_categs']/a[contains(@href,'/listings/')]/text()").extract_first() is not None:
            item['typeImm'] = (response.xpath(
                "//*[@id='all_wrapper']//div[@class='property_categs']/a[contains(@href,'/listings/')]/text()").extract_first())

        # SCRAPING FONDS
        item['fonds'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Garages:')]]/following-sibling::text()").extract_first() is not None:
            item['fonds'] = response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Garages:')]]/following-sibling::text()").extract_first()

        # SCRAPING PLEIN AIR
        item['plein_air'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Construction externe')]]/following-sibling::text()") is not None:
            item['plein_air'] = response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Construction externe:')]]/following-sibling::text()").extract_first()

        # SCRAPING SALLE DE BAIN
        item['salle_de_bain'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Salles de bain:')]]/following-sibling::text()").extract_first() is not None:
            item['salle_de_bain'] = response.xpath(
                "//*[@id='collapseOne']/div[@class='panel-body']/div/*[text()[contains(.,'Salles de bain:')]]/following-sibling::text()").extract_first()

        # SCRAPING CONSTRUCTIBLE
        item['constructible'] = None
        if response.xpath(
                "//*[@id='all_wrapper']//div[@class='property_categs']/a[1]/text()").extract_first() is not None:
            if response.xpath(
                    "//*[@id='all_wrapper']//div[@class='property_categs']/a[1]/text()").extract_first() == "Terrain agricole":
                item['constructible'] = "Agricole"
            elif response.xpath(
                    "//*[@id='all_wrapper']//div[@class='property_categs']/a[1]/text()").extract_first() == "Terrains":
                item['constructible'] = "Constructible"

        # SCRAPING SERVICE
        item['service'] = None

        # SCRAPING CHAUFFAGE
        item['chauffage'] = None

        # SCRAPING CLIMATISATION
        item['climatisation'] = None

        # SCRAPING CUISINE
        item['cuisine'] = None

        # SCRAPING INST SPORT
        item['installations_sportives'] = None

        # SCRAPING TEL
        item['tel'] = None
        if response.xpath(
                "//*[@id='collapseOne']/div/div[strong[contains(text(),'Téléphone De L')]]/text()").extract_first() is not None:
            item['tel'] = response.xpath(
                "//*[@id='collapseOne']/div/div[strong[contains(text(),'Téléphone De L')]]/text()").extract_first()

        # SCRAPING AGENT
        item['agence'] = None
        if response.xpath("//div[@class='agent_detail agent_email_class']/a/text()").extract_first() is not None:
            item['agence'] = response.xpath("//div[@class='agent_detail agent_email_class']/a/text()").extract_first()

            # SCRAPING DESCRIPTION
        item['description'] = None
        fulldesc = response.xpath("//*[@class='wpestate_property_description']/p/text()").extract()
        if fulldesc is not None:
            item['description'] = ""
            for el in fulldesc:
                if el == fulldesc[0]:
                    item['description'] += (str(el))
                else:
                    item['description'] += (" \n" + str(el))

        yield item  # Return the new phonenumber'd item back to scrape
