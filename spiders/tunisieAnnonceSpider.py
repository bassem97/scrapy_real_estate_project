import scrapy


# from realestate_scraper.items import RealestateScraperItem


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


class Spider(scrapy.Spider):
    name = 'tunAncSpider'
    start_urls = [
        'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_order_by=31']

    def parse(self, response):
        listt =  response.css("td table[align='center']")
        for resource in listt:
            # if(resource.css(""))
            item = RealestateScraperItem()
            item['typeImm'] = "####"
            # item['typeImm'] = resource.css("div.info-row.amenities.hide-on-grid p:nth-child(2)::text").get()
            # item['description'] = resource.css("h2.property-title a::text").get()
            # item['price'] = resource.css("span.item-price::text").get()
            # item['agence'] = resource.css("p.prop-user-agent a::text").get()
            # item['link'] = resource.css("div.info-row.phone.text-right a::attr(href)").get()
            # item['adresse'] = resource.css("address.property-address::text").get()
            # item['nbpiece'] = resource.css("p span:nth-child(1)::text").get()
            # item['salle_de_bain'] = resource.css("p span:nth-child(2)::text").get()
            # item['superficie_habitable'] = resource.css("p span:nth-child(3)::text").get()
            yield item
        # next_page = response.css("ul.pagination li:nth-last-child(2) a::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
