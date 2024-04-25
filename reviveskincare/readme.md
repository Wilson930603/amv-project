# reviveskincare Scrapy Spider
This is a Scrapy spider that crawls through the given product urls of `reviveskincare.com` and extracts the title, price and review deatils.

## Installation
- Install python version >= 3.7
- Run the follwoing command to install libs:
```bash
pip install scrapy, pandas, parsel
```
## Usage
Run the spider using the following command in the terminal:
```bash
scrapy crawl reviveskincare -o ./datafolder/reviveskincare.csv
```
the extracted data will be saved in a csv file in datafolder directory.


# Nordstrom Spider
This is a python-request spider that extracts the productId from the given url and gets the reviews from the api using the cookies and headers.

## Installation
- Install python version >= 3.7
- Run the follwoing command to install libs:
```bash
pip install scrapy, pandas, parsel
```

## Usage
- open the script and place the URL whose reviews needs to be scraped. 
- Once the URL is placed run the following command:
```bash
python nordstrom.py
```
