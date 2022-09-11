<h1 align="center">
  RobinWould
 </h1>
<p align="center">
  <em>Spend time thinking, not coding. Scrape data with RobinWould</em>
</p>

<p align="center">
  <a href="https://github.com/xlurio/robinwould/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/xlurio/robinwould/actions/workflows/test.yml/badge.svg" alt="Test"/>
  </a>
  <a href="https://codecov.io/gh/xlurio/robinwould" target="_blank">
    <img src="https://codecov.io/gh/xlurio/robinwould/branch/main/graph/badge.svg?token=941OPKOREQ" alt="Coverage" />
  </a>
  <a href="" target="_blank">
    <img src="https://img.shields.io/pypi/v/robinwould" alt="Package version" />
  </a>
</p>

## Introduction

RobinWould is framework for fast and easy development on web scraping tools based. With less than 10 lines of code you already have script ready to fish for data on the web.


## Requirements

- Python 3.8+
- aiohttp
- Scrapy


## Installing

```
pip install robinwould
```


## Example

### Create it

Create a `main.py` with:

```
from robinwould import Crawler, fields, interfaces

class DataToScrape(interfaces.Model):
    foo = fields.StringField()
    bar = fields.IntegerField()

crawler = Crawler()

@crawler.spider(url="https://www.example.com/")
def mrs_spider(response):
    yield DataToScrape(
        foo='//div[@class="foobar-wrapper" and position()=1]/p[@class="foo"]/text()',
        bar='//div[@class="foobar-wrapper" and position()=1]/p[@class="bar"]/text()'
    )
    
if __name__ == '__main__':
    crawler.run()
```

### Run it

Run the script with:

- On Windows:
```
python main.py
```

- On Linux or MacOS:
```
python3 main.py
```


### Check it

If the spider worked, it should print the scraped data as the follow:

```
Data scraped: {'foo': 'Foo data', 'bar': 2}
```

You just created an script that:
- Downloads the source file from `https://www.example.com/`;
- Scraped the `foo` and `bar` data;

The `crawler.run()` method returns all the scraped data, so if you want to write the data into a file, just assign it to a variable and process it.


## More information

- For learning more about the XPath expressions, you can find it on [Scrapy documentation](https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths).

I'm so sorry for not being able to delivery all the information you may need, I'll be working on a more complete documentation for future versions.


## Licence

This project is licensed under the terms of the MIT license.
