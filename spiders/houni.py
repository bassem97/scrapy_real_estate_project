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
    name = 'houniSpider'
    start_urls = ['https://houni.tn/immobiliers/achat?categories=0&categories=1&categories=3&categories=2&budgetMin=10000&viewType=gallery']
    for i in range(2, 1431):
        start_urls.append(
            'https://houni.tn/immobiliers/achat?categories=0&categories=1&categories=3&categories=2&budgetMin=10000&viewType=gallery&currentPage' + str( i))

    def parse(self, response):
        total_annonce_string = response.css("strong.is-italic::text").get()
        total_annonce_number = int(''.join(filter(lambda i: i.isdigit(), total_annonce_string)))

        list = response.css('div.card')
        for resource in list:
            item = RealestateScraperItem()
            item['link'] = resource.css('a.coveringLink::attr(href)').get()
            item['title'] = resource.css('h5.title.has-text-weight-bold.is-size-5 span span::text').get()
            # if response.css("h4.listingH4.floatR::text").get() is None
            item['adresse'] = resource.css("p.subtitle.is-size-6.has-text-grey-darker.mb-3 span::text").get()
            item['price'] = resource.css("div.card-footer-item.has-text-primary.has-text-weight-bold.is-size-5::text").get()
            item['nbpiece'] = resource.css("div.card-details.has-text-grey-darker.mb-2 div div::text").get()
            item['salle_de_bain'] = resource.css("div.card-details.has-text-grey-darker.mb-2 div:nth-child(2) div::text").get()
            item['superficie_habitable'] = resource.css("div.card-details.has-text-grey-darker.mb-2 div:nth-child(3) div::text").get()

            if resource.css("figure.image.is-3by2 img::attr(src)").get() is not None:
                item['thumbnail_url'] = resource.css("figure.image.is-3by2 img::attr(src)").get()
                item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]
            yield item
        # next_page = response.css("div.load-more-txt").get()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
