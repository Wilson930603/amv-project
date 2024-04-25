# Vietnam Amazon Spiders
The scrapy project consits of two spiders `amazon_urls` and `amazon`. Where `amazon_urls` extracts the product urls from category listing, and `amazon` spider used those urls to extract the products.

## Requirments
Use the following command after installing python>=3.7
```bash
pip install scrapy, pandas
```

## Usage
- First open the spider in terminal
- Add the category url in the amazon_url.py file in start_request
- Execute the spider using the following command.

```bash
scrapy crawl amazon_urls -o ./datafolder/amazon_urls.csv
```
- The urls are extracted and saved in a csv file in `/datafolder/amazon.urls.csv` directory.
- After the urls are extracted then execute the follwing command to extract the product's information

```bash
scrapy crawl amazon_products -o ./datafolder/amazon_dataset.csv
```
- The extracted data will be saved in `./datafolder/amazon_dataset.csv`
