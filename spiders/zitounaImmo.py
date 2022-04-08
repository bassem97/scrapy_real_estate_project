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
    name = 'zitounaImmoSpider'
    start_urls = ['https://zitounaimmo.com/search?vocations%5B%5D=1&reference=&surface_terrain_min=&surface_terrain_max=&prix_min=&prix_max=&cos=&cuf=&etage=&r-etage=' ]

    def parse(self, response):
        list = response.css('div.col-md-6.col-lg-6')
        for resource in list:
            item = RealestateScraperItem()
            item['price'] = resource.css("div.fp_price::text").get()
            if item['price']  == "Prix sur demande" :
                yield None
            else:
                item['link'] = resource.css('a.w-100::attr(href)').get()
                item['title'] = resource.css('h3.couper-mot::text').get()
                item['adresse'] = resource.css('div.tc_content p:nth-child(3)::text').get()


                if resource.css("ul.prop_details.mb0 li:nth-child(3)::text").get()  is not None:
                    item['superficie_habitable'] = resource.css("ul.prop_details.mb0 li:nth-child(3)::text").get()

                if resource.css("ul.prop_details.mb0 li:nth-child(2)::text").get()  is not None:
                    item['salle_de_bain'] = resource.css("ul.prop_details.mb0 li:nth-child(2)::text").get()

                if resource.css("ul.prop_details.mb0 li:nth-child(1)::text").get() is not None:
                    item['nbpiece'] = resource.css("ul.prop_details.mb0 li:nth-child(1)::text").get()


                if resource.css("div.div-img.lazy::attr(data-src)").get() is not None:
                    item['thumbnail_url'] = resource.css("div.div-img.lazy::attr(data-src)").get()

                yield item


        next_page = response.css("div.mbp_pagination ul li:nth-last-child(2) a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
