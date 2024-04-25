# Oracle Forum Web Scraper
This Python script uses Selenium and Parsel libraries to scrape the user and URL data of Oracle Forum. The user and URL data are stored in a CSV file.

# Requirements
- Python > 3.7
- Chrome Browser
- Chrome Driver
- Selenium
- Parsel
- Pandas
- Webdriver-manager


Download the Chrome driver and place it in the same directory as the script.
Run the script using the following command:
```bash
python oracle_forum_scraper.py
```
The script will generate a CSV file with the scraped data.
# Usage
The START_URL variable in the script determines the starting page of the scraping process.
The getQuestionUrls function scrapes the URLs of each forum thread.
The script then scrapes the user and URL data of each forum thread using the URLs obtained from getQuestionUrls function.
The data is stored in a CSV file with the naming convention "oraclelinux_<date>.csv".