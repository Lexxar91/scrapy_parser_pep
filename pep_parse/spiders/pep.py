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

    # Давай здесь лучше воспользуемся встроенными инструментами в модуль,
    # а не будем использовать сплит,
    # а потом делать срезы. Здесь можно поступить, например, вот так:
        # Получить таблицу.
        # И после этого получить number подобным образом:
        # table.css('dt:contains("PEP") + dd::text').get()
        # Тоже самое сделаем и для статуса.

    # Дмитрий, здравствуйте, не смог найти Вас в "пачке", решил написать тут.
    # Я не очень понял какую именно таблицу брать?Которая на странице с PEP-ом?
    # или с главной странице, где полный список PEP-ов?
    # я не смог имплементировать код именно так как писали вы выше.
    # И поняв что главное избавиться от метода split() и срезов
    # сделал чуть подругому,сгенерировал "регулярки" через ChatGPT
    # "прекрутил" их к коду и получился тот же результат.
    def parse_pep(self, response):
        number = response.css('h1.page-title').re(r'<h1.*?>(PEP )(\d{1,4})')
        data = {
            "number": number[1],
            "name": response.css('h1.page-title').re(r'– (.+)</h1>'),
            "status": (response.css('dt:contains("Status") + dd abbr::text')
                       .get())
        }
        yield PepParseItem(data)
