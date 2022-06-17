import scrapy
from pyasn1.type.univ import Null


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
    nbpiece_superficie_habitable = scrapy.Field()
    thumbnail_url = scrapy.Field()
    thumbnail_name = scrapy.Field()
    garage = scrapy.Field()

class Spider(scrapy.Spider):
    name = 'affareSpider'
    start_urls = ['https://www.affare.tn/petites-annonces/tunisie/vente-appartement',
                  'https://www.affare.tn/petites-annonces/tunisie/vente-maison',
                  'https://www.affare.tn/petites-annonces/tunisie/terrain'
                  ]
    for i in range(1,250):
        start_urls.append('https://www.affare.tn/petites-annonces/tunisie/vente-appartement?o='+str(i))

    for i in range(1,363):
        start_urls.append('https://www.affare.tn/petites-annonces/tunisie/vente-maison?o='+str(i))

    for i in range(1,376):
        start_urls.append('https://www.affare.tn/petites-annonces/tunisie/terrain?o='+str(i))

    def parse(self, response):
        list = response.css("div.col-xs-12.col-sm-8 div div:nth-child(3) div.AnnoncesList_product_x__BzrCL   ")
        for resource in list:
            item = RealestateScraperItem()
            item['description'] = resource.css("a div:nth-child(2) div::text").get()
            item['price'] = resource.css("span.AnnoncesList_price__J_vIo::text").get()
            item['adresse'] = resource.css("div.AnnoncesList_section7877o__bOPTn div:nth-child(3) p::text").get()
            item['nbpiece'] = resource.css("div.AnnoncesList_section7877o__bOPTn div:nth-child(3) p:nth-child(2) span::text").get()
            item['superficie_habitable'] = resource.css("div.AnnoncesList_section7877o__bOPTn div:nth-child(3) p:nth-child(2) span:nth-child(2)::text").get()
            item['dateAnnonce'] = resource.css("div.AnnoncesList_section7877o__bOPTn div:nth-child(3) p:nth-child(3)::text").get()
            item['link'] = resource.css("a::attr(href)").get()
            item['typeImm'] = None
            item['gouvernorat'] = None
            item['delegation'] = None
            item['localite'] = None
            item['reference'] =None
            item['nbpiece_superficie_habitable'] =None
            item['thumbnail_url'] =None
            item['thumbnail_name'] =None
            item['garage'] =None
            item['agence'] =None
            item['tel'] =None
            item['constructible'] =None
            item['fonds'] =None
            item['installations_sportives'] =None
            item['climatisation'] =None
            item['salle_de_bain'] =None
            item['chauffage'] =None
            item['plein_air'] =None
            item['service'] =None
            item['typeImm'] =None

            yield item
        next_page = response.css("ul.pagination-lg.pagination li:last-child a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

