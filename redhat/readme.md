# Spider_REDHAT Scrapy Spider
This is a Scrapy spider that crawls through the Red Hat forums (https://access.redhat.com) and scrapes user information. The spider starts from the discussions page and then follows each question to the page with the users who have responded to it.

# Usage
Run the spider using the following command in the terminal:
```bash
scrapy crawl redhat -o ./datafolder/redhat_data.csv
```
