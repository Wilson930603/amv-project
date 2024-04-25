### Linux (Rocky & Almalinux)
This is a Scrapy spider script designed to scrape user information from the AlmaLinux community forum website.

# Requirements
To run this script, you will need to have Python and Scrapy installed on your machine. You can download Python from https://www.python.org/downloads/, and install Scrapy using pip with the following command:

```bash
pip install scrapy
```
# How to use
Navigate to the root directory of the project where the scrapy.cfg file is located.

Run the spider with the following command, replacing <spider_name> with the name of the spider defined in the script:
```bash
scrapy crawl <spider_name> -o ./datafolder/data.csv
```
The results of the spider's output will be saved to a csv file located in the datafolder directory of the project.

# The script uses the following libraries:

scrapy to create the spider and handle HTTP requests and responses
scrapy.http.Request to construct HTTP requests
..items to import the custom item classes used to store the scraped data



