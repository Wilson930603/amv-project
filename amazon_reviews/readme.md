# Script spider.py
This script is a web scraper built using Scrapy for extracting url of products listed on Amazon. It is specifically designed for extracting product URLs from Amazon.com and Amazon.co.uk websites. 

The script uses the following libraries:

- Scrapy for web scraping
- Pandas for data processing and storage
- JSON for data serialization
- random and re for random user agent selection and string manipulations

Usage
To run the script, navigate to the project directory and run the following command in the terminal:

Copy code

```bash
scrapy crawl amazon ./datafolder/data.csv
```
Features
The script extracts productURLs for a specific product by visiting its product page.
The script extracts the following information for each review:
brand
url
The extracted data is saved in a CSV file in datafolder directory
Configuration

name: The name of the spider, set to amazon.
base_urlUS: The base URL of the Amazon.com website.
base_urlUK: The base URL of the Amazon.co.uk website.
headers: HTTP headers used for web scraping. It includes a random user agent selected from a list of user agents.
headers_reviews: HTTP headers used for requesting the reviews. It includes a hard-coded user agent.
error: Counter to keep track of errors encountered during scraping.

# Script justLinks.py
This script is a web scraper built using Scrapy for extracting reviews of products listed on Amazon. It is specifically designed for extracting reviews from Amazon.com and Amazon.co.uk websites. It takes a file with product URLs from extracted from the spider.py spdier and extracts the product information and reviews. All the records will be saved in their respective brand folder.

```bash
scrapy crawl amazon_links
```

# Requirements
- Python 3.x
- Scrapy
- Pandas