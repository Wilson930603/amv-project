# SeekingAlpha Scraping
This spider reads the urls from the excel file and loads the urls. Then uses them to download the pdf files and save them in the downloads directory.

## Requirements
- Install Python. The verison of python should be >=3.7.8
- Open the project folder in the terminal and use the following command.
```bash
pip install -r requirments.txt
```

## Usage
- Open the project folder in the terminal.
- Enter the following command.
```bash
scrapy crawl seekingalpha
```
- The spider will read urls from the excel file and download the pdfs and save them in the `Downloads` directory.

