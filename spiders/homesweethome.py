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


class Spider(scrapy.Spider):
    name = 'homeSweetHomeSpider'
    start_urls = ['https://www.homesweethome.com.tn/search-result-page/?keyword=&status%5B%5D=a-vendre&type%5B%5D=appartement&type%5B%5D=bureau&type%5B%5D=condo&type%5B%5D=depot&type%5B%5D=duplex&type%5B%5D=etage-de-villa&type%5B%5D=fond-de-commerce&type%5B%5D=hotel&type%5B%5D=immeuble&type%5B%5D=investissement&type%5B%5D=local-commercial&type%5B%5D=loft&type%5B%5D=maison-de-vacances&type%5B%5D=parking&type%5B%5D=quadruplex&type%5B%5D=rdc-de-villa&type%5B%5D=studio&type%5B%5D=terrain-agricole&type%5B%5D=terrain-commercial&type%5B%5D=terrain-industriel&type%5B%5D=terrain-loisir&type%5B%5D=terrain-promoteur&type%5B%5D=terrain-villa&type%5B%5D=triplex&type%5B%5D=usine&type%5B%5D=villa&bedrooms=&bathrooms=&min-price=&max-price=&property_id=',
                  ]

    def parse(self, response):
        list = response.css('div.item-listing-wrap')
        for resource in list:
            item = RealestateScraperItem()
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
            item['cuisine'] = None
            item['anneeConst'] = None
            item['description'] = None
            item['dateAnnonce'] = None
            item['link'] = resource.css('h2.item-title a::attr(href)').get()
            item['title'] = resource.css('h2.item-title a::text').get()
            item['adresse'] = resource.css("address::text").get()
            item['price'] = resource.css("li.item-price::text").get()
            item['salle_de_bain'] = resource.css("li.h-baths span:nth-child(3)::text").get()
            item['nbpiece'] = resource.css("li.h-beds span:nth-child(3)::text").get()
            item['superficie_habitable'] = resource.css("li.h-area span:nth-child(2)::text").get()
            item['typeImm'] = resource.css("li.h-type span::text").get()
            if resource.css("img.img-fluid.wp-post-image::attr(src)").get() is not None:
                item['thumbnail_url'] = resource.css("img.img-fluid.wp-post-image::attr(src)").get()
            else:
                item['thumbnail_url'] = None

            yield item
        next_page = response.css("ul.pagination.justify-content-center li:nth-last-child(2) a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
