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
    image = scrapy.Field()
    thumbnail_url = scrapy.Field()
    thumbnail_name = scrapy.Field()



class Spider(scrapy.Spider):
    name = 'newKeySpider'
    start_urls = ['https://www.newkey.com.tn/search?vocations=1&reference=&bathrooms=&prix_min=&prix_max=']


    def parse(self, response):
        list = response.css("div.property-listing.list-view div.row div.item-wrap.infobox_trigger")
        for resource in list:
            item = RealestateScraperItem()
            item['delegation'] = None
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
            item['typeImm'] = resource.css("div.info-row.amenities.hide-on-grid p:nth-child(2)::text").get()
            item['description'] = resource.css("h2.property-title a::text").get()
            item['price'] = resource.css("span.item-price::text").get()
            item['link'] = resource.css("div.info-row.phone.text-right a::attr(href)").get()
            item['gouvernorat'] = resource.css("address a:nth-child(1)::text").get()
            item['delegation'] = resource.css("address a:nth-child(1)::text").get()
            item['localite'] = resource.css("address a:nth-child(1)::text").get()
            item['nbpiece'] = resource.css("span.h-beds span::text").get()
            item['superficie_habitable'] = resource.css("span.h-area span::text").get()
            item['reference'] = resource.css("span.label-status.label-status-109.label.label-default a::text").get()
            item['thumbnail_url'] = resource.css("div.div-img::attr(style)").get().split('(')[-1].replace(')', '')
            item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]
            yield item
        next_page = response.css("ul.pagination li:nth-last-child(2) a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

