import scrapy

class EcommerceSpider(scrapy.Spider):
    name = 'ecommerce_spider'
    start_urls = ['https://www.spinneyslebanon.com/default/alcohol.html',
                  'https://www.spinneyslebanon.com/default/beverages.html',
                  'https://www.spinneyslebanon.com/default/bakery.html',
                  'https://www.spinneyslebanon.com/default/deli-dairy-eggs.html',
                  'https://www.spinneyslebanon.com/default/fruits-vegetables.html',
                  'https://www.spinneyslebanon.com/default/meat-seafood.html',
                  'https://www.spinneyslebanon.com/default/frozen.html',
                  'https://www.spinneyslebanon.com/default/food-cupboard.html']  # Replace with the actual URL of the product listing page

    def parse(self, response):
        # Extract the product URLs from the listing page
        product_urls = response.css(".product-item-info").css("::attr(href)").re(".*.html")

        # Follow each product URL and extract fields
        for url in product_urls:
            yield scrapy.Request(url, callback=self.parse_product)

        # Follow pagination links if available
        next_page_url = response.css('.next::attr(href)').get()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        # Extract fields from the product page
        title = response.css('.base::text').get()
        price = response.css('.price::text').get()
        description = response.css('div.value::text').get()
        image_url = response.css(".imgzoom::attr(data-zoom)").get()
        brand = response.css("span.prod_brand a ::text").get()
        quantity = response.css("span.prod_brand ::text").get() + " " + response.css("span.prod_weight::text").get()
        about_the_brand = response.css("span.brand_base_text ::text").get()
       # nutritional_facts = response.css('div.nutritionalFacts#nutritionalFacts::text').get()

        # Process or store the extracted data as needed
        yield {
            'title': title,
            'price': price,
            'description': description,
            'image_url' : image_url,
            'quantity':quantity,
            'brand':brand,
            'about_the_brand':about_the_brand
        }
