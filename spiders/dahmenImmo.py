import scrapy




# from realestate_scraper.items import RealestateScraperItem


class RealestateScraperItem(scrapy.Item):
    # default_input_processor = MapCompose(unicode.strip)
    # define the fields for your item here like:
    title = scrapy.Field()  #
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
    thumbnail_url = scrapy.Field()
    thumbnail_name = scrapy.Field()
    nbpiece_superficie_habitable = scrapy.Field()
    garage = scrapy.Field()


class Spider(scrapy.Spider):
    name = 'dahmenImmoSpider'
    start_urls = ['https://www.dahmenimmobilier.tn/search/liste?property_types%5B%5D=1&property_types%5B%5D=5&property_types%5B%5D=10&property_types%5B%5D=11&vocations%5B%5D=1&reference=' ]

    def parse(self, response):
        list = response.css('div.list-offer')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('a.list-offer-left::attr(href)').get()
            item['title'] = resource.css('h4.list-offer-title.couper-mot::text').get()
            item['adresse'] = resource.css("div.list-offer-h4 h4:nth-child(2)").get()
            item['price'] = resource.css("div.list-price::text").get()
            item['reference'] = resource.css("div.reference::text").get()
            item['typeImm'] = resource.css("div.estate-type::text").get()

            if resource.css("div.list-area").get() is not None:
                item['superficie_habitable'] = resource.css("div.list-area").get()
            else :
                item['superficie_habitable'] = None

            if resource.css("div.list-rooms").get() is not None:
                item['nbpiece'] = resource.css("div.list-rooms").get()
            else :
                item['nbpiece'] = None

            if resource.css("div.list-offer-photo::attr(style)").get() is not None:
                item['thumbnail_url'] = resource.css("div.list-offer-photo::attr(style)").get()
            else :
                item['thumbnail_url'] = None

            item['typeImm'] = None
            item['gouvernorat'] = None
            item['delegation'] = None
            item['localite'] = None
            item['reference'] = None
            item['nbpiece_superficie_habitable'] = None
            item['agence'] = None
            item['tel'] = None
            item['constructible'] = None
            item['fonds'] = None
            item['installations_sportives'] = None
            item['climatisation'] = None
            item['chauffage'] = None
            item['plein_air'] = None
            item['service'] = None
            item['salle_de_bain'] = None
            item['cuisine'] = None
            item['anneeConst'] = None
            item['description'] = None
            item['dateAnnonce'] = None

            yield item
        next_page = response.css("div.offer-pagination.margin-top-30 a:nth-last-child(2)::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
