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
    thumbnail_url = scrapy.Field()
    thumbnail_name = scrapy.Field()
    nbpiece_superficie_habitable = scrapy.Field()



class Spider(scrapy.Spider):
    name = 'mubawabSpider'
    start_urls = ['https://www.mubawab.tn/fr/cc/immobilier-a-vendre-all:prmn:%3E60000:sc:apartments-for-sale,commercial-property-for-sale,farms-for-sale,houses-for-sale,land-for-sale,offices-for-sale,riads-for-sale,villas-and-luxury-homes-for-sale']
    # for i in range(1,250):
    #     start_urls.append('https://www.affare.tn/petites-annonces/tunisie/vente-appartement?o='+str(i))



    def parse(self, response):
        list = response.css('div.col-9 ul.ulListing li.listingBox.w100')
        for resource in list:
            item = RealestateScraperItem()
            item['description'] = resource.css("p.listingP.descLi::text").get()
            # if response.css("h4.listingH4.floatR::text").get() is None
            item['price'] = resource.css("span.priceTag.hardShadow.float-right.floatL::text").get()
            item['adresse'] = resource.css("h3.listingH3::text").get()
            item['nbpiece_superficie_habitable'] = response.css("h4.listingH4.floatR::text").get()
            item['link'] = resource.css("li.listingBox.w100::attr(linkref)").get()
            if resource.css("img.w100.sliderImage.firstPicture::attr(data-url)").get() is not None:
                item['thumbnail_url'] = resource.css("img.w100.sliderImage.firstPicture::attr(data-url)").get()
                item['thumbnail_name'] = item['thumbnail_url'].split('/')[-1]

            yield item
        next_page = response.css("div.paginationDots.sMargTop.centered a:last-child::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

