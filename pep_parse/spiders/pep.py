import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_pep = response.xpath('//section[@id="numerical-index"]')
        tbody = all_pep.css('tbody')
        href = tbody.css('a::attr(href)')
        for link in href:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number_and_title = response.css('h1.page-title::text').get()
        number_pep = number_and_title.split()
        title_pep = number_and_title.split()
        data = {
            "number": number_pep[1],
            "name": title_pep[3:],
            "status": response.css('abbr::text').get()
        }

        yield PepParseItem(data)
