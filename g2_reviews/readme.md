# G2 reviews
This script is a Python script that uses the Scrapy library to scrape reviews from g2 website.

# Installation
To use this script, you'll need to have Python and the Scrapy library installed on your system.

Install Python. You can download the latest version of Python from the official website: https://www.python.org/downloads/
Install Scrapy. You can install Scrapy using pip by running the following command in your terminal: 
```bash
pip install scrapy
```
# Usage
To run the script, navigate to the directory in your terminal and run the following command:
```bash
scrapy crawl g2_reviews -o g2_reviews.csv
```
This will start the spider and scrape data from the Centos forums. The data will be output to the console and saved to g2_reviews.csv.