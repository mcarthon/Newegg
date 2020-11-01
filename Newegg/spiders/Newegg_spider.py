from scrapy import Request, Spider
from Newegg.items import NeweggItem

class NeweggSpider(Spider):
    name = 'Newegg_spider'
    start_urls = ["https://www.newegg.com/p/pl?d=monitors&PageSize=96&page=1"]
    allowed_urls = ["https://www.newegg.com"]

    def parse(self, response):
        num_pages = int(response.xpath('//div[@class="list-tool-pagination"]/span').xpath('./strong/text()')[2].extract())
        url_list = [f"https://www.newegg.com/p/pl?d=monitors&PageSize=96&page={i+1}" for i in range(num_pages - 2)]

        for url in url_list:
           yield Request(url = url, callback = self.parse_result_page)

    def parse_result_page(self, response):
        products = response.xpath('//div[@class="item-branding"]/a/@href').extract() 
        product_urls = list(filter(lambda url: url.find('FullInfo') != -1, products))
        
        for url in product_urls:
            yield Request(url = url, callback = self.parse_product_page)

    def parse_product_page(self, response):
        try:
            product_name = response.xpath('//h1[@class="product-title"]/text()').extract()
        except:
            print('*****Could not find product name!*****')
            product_name = None

        try:
            price = float(response.xpath('//li[@class="price-current"]/strong/text()').extract_first()) + float(response.xpath('//li[@class="price-current"]/sup/text()').extract_first())
        except:
            print('*****Could not find price*****')
            price = None
        
        try:
            product_specs = response.xpath('//div[@class="product-bullets"]/ul/li/text()').extract()
            resolution = list(filter(lambda spec: spec.find('Resolution') != -1, product_specs))
            response_time = list(filter(lambda spec: spec.find('Response Time') != -1, product_specs))
            refresh_rate = list(filter(lambda spec: spec.find('Refresh Rate') != -1, product_specs))
            video_inputs = list(filter(lambda spec: spec.find('Video Inputs') != -1, product_specs))
            flicker_free = list(filter(lambda spec: spec.find('Flicker-Free') != -1, product_specs))
            screen_curvature = list(filter(lambda spec: spec.find('Curvature') != -1, product_specs))
            mount_compatible = list(filter(lambda spec: spec.find('Mount') != -1, product_specs))
            adjustable = list(filter(lambda spec: spec.find('Adjustable') != -1, product_specs))
        except:
            print('*****Could not find product specs*****')

        try:
            review_count =  int(response.xpath('//div[@class="product-reviews"]//span//text()').extract()[1])
        except:
            print('*****Could not find review count*****')
            review_count = None

        try:
            review_rating = float(response.xpath('//div[@class="product-reviews"]//i').extract_first()[24])
        except:
            print('Could not find review rating*****')
            review_rating = None

        item = NeweggItem()
        item['product_name'] = product_name
        item['price'] = price
        item['resolution'] = resolution
        item['response_time'] = response_time
        item['refresh_rate'] = refresh_rate
        item['video_inputs'] = video_inputs
        item['flicker_free'] = flicker_free
        item['screen_curvature'] = screen_curvature
        item['mount_compatible'] = mount_compatible
        item['adjustable'] = adjustable
        item['review_count'] = review_count
        item['review_rating'] = review_rating

        yield item


        
