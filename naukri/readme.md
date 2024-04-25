# Naukri.com Spider
This script is a web scraping spider implemented using Scrapy, a Python framework for scraping websites. The spider is designed to crawl the Naukri.com website and extract job listing information.

# Prerequisites
Before running the script, ensure that you have the following prerequisites installed:

- Python 3.x
- Scrapy
- pytz

# Installation
Clone or download the repository containing the script.

Install the required dependencies by running the following command:

Copy code
```bash
pip install scrapy pytz
```
# Usage
Open the terminal or command prompt and navigate to the directory where the script is located.

Run the spider using the following command:

Copy code
```bash
scrapy crawl naukri_com
```
The spider will start crawling the Naukri.com website and extracting job listing information.

The extracted data will be saved in the naukri.json file in the same directory as the script.

Configuration
The script contains the following configurable parameters:

allowed_domains: The list of allowed domains for the spider. You can modify it to specify the target domain.

start_urls: The list of start URLs for the spider. You can modify it to specify the initial URLs to crawl.

handle_httpstatus_list: The list of HTTP status codes to handle. You can modify it to specify the desired status codes.

cookies: The cookies required for authentication and session management. You can modify it with the necessary cookies.

headers: The headers to be sent with the requests. You can modify it to customize the headers as needed.

Output
The script outputs the extracted data in JSON format. Each job listing is represented as a separate JSON object in the output file.

The output file (naukri.json) will contain the following fields for each job listing:

job_title: The title of the job.
company_name: The name of the company.
location: The location of the job.
experience: The required experience for the job.
posted_on: The date when the job was posted.
Notes
The script includes a specific set of cookies and headers that were present at the time of writing. Please ensure that the cookies and headers are up to date for successful execution.

The script may need modifications if there are changes in the target website's structure or authentication mechanism.

Respect the website's terms of service and scraping policies while using this script.

For more information on Scrapy, refer to the Scrapy documentation.





