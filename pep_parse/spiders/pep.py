import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_pep = response.css('section#numerical-index')
        tbody = all_pep.css('tbody')
        href = tbody.css('a::attr(href)')
        for link in href:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.css('h1.page-title').re(r'<h1.*?>(PEP )(\d{1,4})')
        data = {
            "number": number[1],
            "name": response.css('h1.page-title').re(r'– (.+)</h1>'),
            "status": (response.css('dt:contains("Status") + dd abbr::text')
                       .get())
        }
        yield PepParseItem(data)
