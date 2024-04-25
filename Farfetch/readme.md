# Farfetch Scraper
This Python script allows you to scrape product data from farfetch.com.

# Installation
To use the script, you need to have Python 3.x installed on your system. You can download Python from the official website python.org.

You also need to install the following Python packages:

pandas
tqdm
selenium

You can install these packages using the following command:

Copy code
```bash
pip install pandas tqdm selenium
```
You also need to have Chrome WebDriver installed on your system.

Usage
Before using the script, you need to modify the following variables in the script:

TYPE_RUN: 1 or anyother digit (1 for productUrl extraction. and anyother digit for product extraction)
FILE_NAME: path of the file that needs to be used for extraction (should be according to the TYPE_RUN).
THREAD_COUNT: Number of threads
To run the script, open a command prompt or terminal window and navigate to the directory containing the script. Then run the following command:

Copy code
```bash
python farfetch_scraper.py
```

Output
The script outputs two CSV files:

./productUrls/listing_farfetch_{date}_{number}_final.csv: Contains a list of product URLs scraped from farfetch.com.
./productData/Data_farfetch_{date}_{number}_final.csv: Contains the scraped product data, including the main category, brand, product category, product subcategory, product name, and price.


# More Instruction

This code can be run in two modes, one to extract product links when the TYPE_COUNT =0, and if not 0 then it extracts the product data from the website. The file name for the relavent type should be given to run the script. THREAD_COUNT is the number of threads you can create for extraction on both modes. If in some case the code exexcution is stopped, then it can continue from where it was stooped, just have to make sure that the date in the extracted file should be the same as current date. 
Before running this file, extracting_main.py should be exexcuted to extract categories, and then extract_product_listing.py should be executed to extract the product listing. After the first two the extractingproduct.py should be run in TYPE_COUNT 0, and once that finishes then it should be run with TYPE_COUNT 1.


