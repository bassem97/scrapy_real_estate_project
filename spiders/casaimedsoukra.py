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
    name = 'casaimedsoukraSpider'
    start_urls = ['https://casaimedsoukra.com/vente/appartement',
                  'https://casaimedsoukra.com/vente/villa',
                  'https://casaimedsoukra.com/vente/terrain',
                  'https://casaimedsoukra.com/vente/commerciale',
                  'https://casaimedsoukra.com/vente/bureau'
                  ]

    def parse(self, response):
        list = response.css('div.col-xs-12.col.isoCol.sale')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('h2.fontNeuron.text-capitalize a::attr(href)').get()
            item['title'] = resource.css('h2.fontNeuron.text-capitalize a::text').get()
            item['adresse'] = resource.css("p.couper-mot::text").get()
            item['price'] = resource.css("span.textSecondary::text").get()

            if resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(2) strong:nth-child(2)::text").get() is not None:
                item['nbpiece'] = resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(2) strong:nth-child(2)::text").get()

            if resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(1) strong:nth-child(2)::text").get() is not None:
                item['superficie_habitable'] = resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(1) strong:nth-child(2)::text").get()

            item['reference'] = resource.css("span.btn.btnSmall.btn-info.text-capitalize::text").get()

            if resource.css("div.imgHolder::attr(style)").get() is not None:
                item['thumbnail_url'] = resource.css("div.imgHolder::attr(style)").get()

            yield item
        next_page = response.css("li.next.page-numbers a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
