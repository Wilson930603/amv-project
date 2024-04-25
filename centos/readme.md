# CentossSpider
This script is a Python script that uses the Scrapy library to scrape data from the Centos forums. It defines a Scrapy spider named "CentossSpider" that scrapes information from the forum threads, including the URL, title, user, user URL, date, posts, and joined date.

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
scrapy crawl centoss -o centoss.csv
```
This will start the spider and scrape data from the Centos forums. The data will be output to the console and saved to centoss.csv.