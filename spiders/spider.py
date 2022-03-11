import scrapy


class Spider(scrapy.Spider):
    name = 'YosraSpider'
    start_urls = ['https://www.yosra.tn/en/']

    def parse(self, response, **kwargs):
        matches = ["/", "Price on request", "From"]
        for products in response.css('div.infos'):
            if not any(x in products.css('p::text').get() for x in matches):
                yield {
                    'title': products.css('div>h4::text').get(),
                    'price': products.css('p::text').get().replace(' DT', ''),
                    'link': products.css('ul.ads>li>a::attr(href)').get(),
                }
