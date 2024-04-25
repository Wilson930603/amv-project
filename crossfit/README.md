# Prepare the environment
1. Install Python 3.7.4 or above.
2. Install the required packages:
```
pip install -r requirements.txt
```

# Run the script
```
scrapy crawl crossfit
```

# Clean the results
```
python clean.py
```

# Output
1. The results are saved in the `data.csv` file.
2. The cleaned results are saved in the `data_cleaned.csv` file.

# About the data
1. The non cleaned data contains City, State and Zip as separate columns and some extra informations.
2. The cleaned data contains City, State and Zip as a single column and only the required informations.
3. The cleaned data only has 3 countries: USA, Australia and New Zealand.

