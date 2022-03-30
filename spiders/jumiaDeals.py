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
    image = scrapy.Field()
    thumbnail_url = scrapy.Field()
    thumbnail_name = scrapy.Field()



class Spider(scrapy.Spider):
    name = 'jumiaDealSpider'
    start_urls = ['https://deals.jumia.com.tn/appartements-a-vendre',
                  'https://deals.jumia.com.tn/maisons-a-vendre',
                  'https://deals.jumia.com.tn/terrains-parcelles',
                  'https://deals.jumia.com.tn/locaux-commerciaux-bureaux'
                  ]


    def parse(self, response):
        list = response.css("article.post-holder.product-click")
        for resource in list:
            item = RealestateScraperItem()
            item['title'] = resource.css("a.post-link.post-vip span::text").get()
            item['adresse'] = resource.css("span.address::text").get()
            item['dateAnnonce'] = resource.css("span.address::text").get()
            item['description'] = resource.css("h2.property-title a::text").get()
            item['price'] = resource.css("span.price::text").get()
            item['dateAnnonce'] = resource.css("time::text").get()
            item['link'] = resource.css("div.info-row.phone.text-right a::attr(href)").get()
            if resource.css("img.product-images::attr(data-src)").get() is not None:
                item['thumbnail_url'] = resource.css("img.product-images::attr(data-src)").get()
                item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]
            yield item
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

