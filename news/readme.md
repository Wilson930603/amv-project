# Shephard Spider and startfor spider
This is a Scrapy spider that crawls the news articles from the website https://www.shephardmedia.com/. It extracts the article's title, category, date, and URL.

Prerequisites
- Python 3.x
- Scrapy
# Usage
Install the requirements by running pip install -r requirements.txt
Run the spider for shephard by executing the command 
```bash
scrapy crawl shephard -o ./datafolder/shephard.csv
```
Run the spider for startfor by executing this command
```bash
scrapy crawl startfor -o ./datafolder/startfor.csv
```
The spider will start scraping the website and will output the extracted data in csv format to the console. You can also specify an output file for the scraped data by appending the -o filename.json flag to the scrapy crawl command.

# Spider Details for shephard
The spider is named shephard.
The starting URL is https://www.shephardmedia.com.
The spider uses a header with various browser properties to mimic a browser request and prevent getting blocked.
The spider starts by calling the pagination method to scrape multiple pages.
The pagination method generates URLs for 1950 pages and calls the parse method for each page.
The parse method extracts the article's title, category, date, and URL by using XPath selectors and regular expressions to clean up the date.
The extracted data is stored in a NewsItem object and yielded to the Scrapy pipeline.

# Spider Details for Startfor
The spider starts by sending a POST request to https://worldview.stratfor.com/api/next-api/content/list with a payload containing search parameters, such as the page number, offset, and limit of the search. The response is parsed as JSON.
The spider then extracts the relevant information from each news article in the response and creates a NewsItem object with the following fields:
Category: the category of the news article.
Title: the title of the news article.
Date: the date of the news article in the format dd/mm/yyyy.
URL: the URL of the news article.
If the response contains no news articles, flag is set to False and the spider stops scraping.

