# Visa Scraping
The is a scrapy spider that reads urls from `links.csv` and extracts name, description, website, capabilities, and countries.

### Requirments
Download python >= 3.7.8 and install the follwing modules:
```bash
pip install scrapy pandas
```

### Usage
To run the spider, open the folder in terminal, and enter the following command.
```bash
scrapy crawl visa -o ./datafolder/visa.csv
```
the spider will run and save the extracted data in visa.csv file in datafolder directory.