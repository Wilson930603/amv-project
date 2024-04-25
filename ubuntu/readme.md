# Ubuntu user scraping scripts

# # Script linkExtractor_users.py
This is a Python script designed to scrape user profile links from the Ask Ubuntu website using proxies and threading for efficiency.

# Prerequisites
Before running the script, ensure that you have the following installed:

- Python 3.6 or higher
- The requests, pandas, and scrapy libraries

# Installation
To install the necessary libraries, run the following command:
```bash
pip install requests pandas scrapy
```

# Usage
- Create a file named proxy.txt in the same directory as the script, and add your proxy IP addresses and ports to it, with one proxy per line.
- Update the question_pages and user_pages variables in the script to reflect the number of pages of questions and user profiles you want to scrape, respectively.
- Run the script using the following command:
```bash
python linkExtractor_users.py
```

The script will output the scraped user profile links to a CSV file named links_users.csv.

# Script dataExtracter_users.py
This Python script is designed to scrape data from AskUbuntu website about StackOverflow users. It uses a list of URLs provided in a CSV file as input and then extracts user information such as the duration of membership on StackOverflow (in years and months) and saves it to a CSV file.

# Functionality:

- The script reads the list of URLs from the input CSV file and sends a GET request to each URL.
- It uses a random proxy from a list of proxies stored in a text file to avoid getting blocked by the server due to frequent requests.
- It extracts user information such as the duration of membership on StackOverflow (in years and months) using XPath selectors.
- The extracted data is saved in a CSV file.
- The script uses multi-threading to increase the speed of scraping. The number of threads can be adjusted using the thread_count variable in the script.

# Usage:

- Place the script in a directory with the following files:
- links_users.csv: A CSV file containing a list of StackOverflow user profile links to scrape.
- proxy.txt: A text file containing a list of proxies to use for scraping.
- Update the thread_count variable to the desired number of threads to use for scraping.
- Run the script. The scraped data will be saved to a CSV file named Users_data.csv in the same directory as the script.

Limitations:
The script may be blocked by the server if too many requests are sent in a short period. To avoid this, use a large list of proxies and set a longer timeout for requests.