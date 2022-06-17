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
    name = 'ayoubImmoSpider'
    start_urls = ['https://ayoubimmobilierhammamet.com/search?reference=&vocations%5B%5D=1&surface_terrain_min=&surface_terrain_max=&prix_min=&prix_max=' ]

    def parse(self, response):
        list = response.css('div.col-md-6.col-lg-6.item-remove')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('a.couper-mot::attr(href)').get()
            item['title'] = resource.css('div.thum_title h5::text').get()
            item['adresse'] = resource.css("div.thum_title p").get()
            item['price'] = resource.css("div.area_price.price_position strong::text").get()

            if resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(1) span::text").get() is not None:
                item['superficie_habitable'] = resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(1) span::text").get()
            else :
                item['superficie_habitable'] = None

            if resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(3) span::text").get() is not None:
                item['salle_de_bain'] = resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(3) span::text").get()
            else :
                item['salle_de_bain'] = None

            if resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(2) span::text").get() is not None:
                item['nbpiece'] = resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(2) span::text").get()
            else:
                item['nbpiece'] = None

            if resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(4) span::text").get() is not None:
                item['garage'] = resource.css("div.thum_data.bg-gray.mt_15 ul li:nth-child(4) span::text").get()
            else:
                item['garage'] = None

            if resource.css("div.div-img.lazy::attr(data-src)").get() is not None:
                item['thumbnail_url'] = resource.css("div.div-img.lazy::attr(data-src)").get()
            else:
                item['thumbnail_url'] = None


            item['typeImm'] = None
            item['gouvernorat'] = None
            item['delegation'] = None
            item['localite'] = None
            item['reference'] =None
            item['nbpiece_superficie_habitable'] =None
            item['agence'] =None
            item['tel'] =None
            item['constructible'] =None
            item['fonds'] =None
            item['installations_sportives'] =None
            item['climatisation'] =None
            item['chauffage'] =None
            item['plein_air'] =None
            item['service'] =None


            yield item
        next_page = response.css("div.nav_pages a:nth-last-child(2)::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

            # default_input_processor = MapCompose(unicode.strip)
            # define the fields for your item here like:

