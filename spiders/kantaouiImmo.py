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
    name = 'kantaouiImmoSpider'
    start_urls = ['https://kantaouiimmo.com/search?vocations%5B%5D=1&reference=&prix_min=&prix_max=&surface_min=&surface_max=' ]

    def parse(self, response):
        list = response.css('div.listing-item')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('a.listing-img-container::attr(href)').get()
            item['title'] = resource.css('h4.couper-mot a::text').get()
            item['adresse'] = resource.css("div.listing-title").get().split('>')[-2]
            item['price'] = resource.css("span.listing-price::text").get()

            if resource.css("ul.listing-features span::text").get() is not None:
                item['superficie_habitable'] = resource.css("ul.listing-features span::text").get()

            if resource.css("ul.listing-features span:nth-child(4)::text").get() is not None:
                item['nbpiece'] = resource.css("ul.listing-features span:nth-child(4)::text").get()

            item['typeImm'] = resource.css("div.listing-badges span:nth-child(2)::text").get()

            if resource.css("div.img-slider-list::attr(style)").get() is not None:
                item['thumbnail_url'] = resource.css("div.img-slider-list::attr(style)").get()

            yield item
        next_page = response.css("nav.pagination ul li:nth-last-child(2) a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
