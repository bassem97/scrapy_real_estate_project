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
    name = 'tunisiePromoSpider'
    start_urls = ['https://www.tunisiapromo.com/recherche?listing_type=4&property_type=1&realtor_type=ANY&isearch=0&region1=ANY&plot_area_min=&plot_area_max=&floor_area_min=&floor_area_max=&bedrooms_min=&bedrooms_max=&year_built_min=&year_built_max=2022&roofs_min=&roofs_max=&price_min=&price_max=&property_search=Filtrer']
    # for i in range(2, 1431):
    #     start_urls.append(
    #         'https://houni.tn/immobiliers/achat?categories=0&categories=1&categories=3&categories=2&budgetMin=10000&viewType=gallery&currentPage' + str( i))

    def parse(self, response):
        # total_annonce_string = response.css("strong.is-italic::text").get()
        # total_annonce_number = int(''.join(filter(lambda i: i.isdigit(), total_annonce_string)))

        list = response.css('article.short_ad_panel')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('a.headline::attr(href)').get()
            item['title'] = resource.css('a.headline::text').get()
            # if response.css("h4.listingH4.floatR::text").get() is None
            item['adresse'] = resource.css("div.property_location.mtop b::text").get()
            item['description'] = resource.css("p.listing-description::text").get()
            item['dateAnnonce'] = resource.css("span.listing_added::text").get()
            item['price'] = resource.css("span.price::text").get()
            if resource.css("img.photo::attr(data-original)").get() is not None:
                item['thumbnail_url'] = resource.css("img.photo::attr(data-original)").get()
                item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]

            yield item

        # next_page = response.css("div.load-more-txt").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    # def getDetails(self):