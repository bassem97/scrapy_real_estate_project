import scrapy
from selenium import webdriver
driver = webdriver.Chrome()



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
    name = 'cavaSpider'
    start_urls = ['https://cava.tn/category/immobilier/appartemen']

    def parse(self, response):
        list = response.css('div.col-xs-12.col-sm-12.col-md-12.col-lg-12.no-hor-padding div#fh5co-board div.columncls')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css(
                'div.image-grid.col-xs-12.col-sm-12.col-md-12.col-lg-12.no-hor-padding a::attr(href)').get()
            item['title'] = resource.css(
                'div.item-name.col-xs-12.col-sm-12.col-md-12.col-lg-12.no-hor-padding.pro_title a::text').get()
            # if response.css("h4.listingH4.floatR::text").get() is None
            item['price'] = resource.css("div.price.bold.col-xs-12.col-sm-12.col-md-12.col-lg-12.no-hor-padding.pro_price span:nth-child(2)").get()
            item['adresse'] = resource.css("span.product-location::text").get()
            if resource.css("img.imgcls::attr(src)").get() is not None:
                item['thumbnail_url'] = resource.css("img.imgcls::attr(src)").get()
                item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]
            yield item
        # next_page = response.css("div.load-more-txt").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
