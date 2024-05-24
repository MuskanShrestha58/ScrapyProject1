import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")
        for book in books:
            yield {
                'title': book.xpath(".//h3/a/@title").get(),
                'url': book.xpath(".//h3/a/@href").get(),
                'price': book.xpath(".//p[@class='price_color']/text()").get(),
            }

        '''
        We're looking for the next button and 
        the below xpath points to the url contained by the next button. 
        '''
        next_page=  response.xpath("//li[@class='next']/a/@href").get()

        #We do this untill we reach the last page where there is no next button
        if next_page is not None:
            # there are two types of url in the website in the next button
            # one looks like "catalogue/page-2.html"
            # other looks like "page-5.html"
            if 'catalogue/' in next_page:
                next_page_url= 'https://books.toscrape.com/'+ next_page
            else:
                next_page_url='https://books.toscrape.com/catalogue/'+ next_page
           
            """
           
             response.follow tells scrapy to go to the url contained 
            by the next_page_url.
            Then, the callback= self.parse calls the above parse function and
            hence all the content of the next and next... pages get scraped .
        
            """

            yield response.follow(next_page_url, callback= self.parse)