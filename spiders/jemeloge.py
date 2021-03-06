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
    name = 'jemelogeSpider'
    start_urls = ['https://www.jemeloge.tn/achat-immobilier?l='];

    def parse(self, response):
        for item in self.scrape(response):
            yield item
            # list = response.css('div.result')
            # for resource in list:
            #     item = RealestateScraperItem()
            #     item['link'] = resource.css('h2 a.title::attr(href)').get()
            #     item['title'] = resource.css('h2 a.title::text').get()
            # item['adresse'] = resource.css("address::text").get()
            # item['price'] = resource.css("li.item-price::text").get()
            # item['salle_de_bain'] = resource.css("li.h-baths span:nth-child(3)::text").get()
            # item['nbpiece'] = resource.css("li.h-beds span:nth-child(3)::text").get()
            # item['typeImm'] = resource.css("li.h-type span::text").get()
            # item['agence'] = resource.css("div.item-author a::text").get()
            #
            # if resource.css("li.h-area span:nth-child(2)::text").get() is not None:
            #     item['superficie_habitable'] = resource.css("li.h-area span:nth-child(2)::text").get()

            # if resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(2) strong:nth-child(2)::text").get() is not None:
            #     item['nbpiece'] = resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(2) strong:nth-child(2)::text").get()
            #
            # if resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(1) strong:nth-child(2)::text").get() is not None:
            #     item['superficie_habitable'] = resource.css("footer.postColumnFoot  ul.list-unstyled li:nth-child(1) strong:nth-child(2)::text").get()

            # item['reference'] = resource.css("span.btn.btnSmall.btn-info.text-capitalize::text").get()

            # if resource.css("img.img-fluid.wp-post-image::attr(src)").get() is not None:
            #     item['thumbnail_url'] = resource.css("img.img-fluid.wp-post-image::attr(src)").get()

            yield item
        # next_page = response.css("ul.pagination.justify-content-center li:nth-last-child(2) a::attr(href)").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def scrape(self, response):
        print("---------------scraping annonces dans une page-------------")
