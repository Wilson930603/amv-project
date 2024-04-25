import pandas as pd


data = pd.read_csv('data.csv')
data = data[['Name', 'Website', 'Address', 'City', 'State', 'Zip', 'Country', 'Phone']]
data['City'] = data[['City', 'State', 'Zip']].apply(lambda x: f'{x["City"]}, {x["State"]} {x["Zip"]}', axis=1)
data = data.drop(columns=['State', 'Zip'])
# replace all characters except numbers
data['Phone'] = data['Phone'].str.replace(r'\D+', '')
data['Website'] = data['Website'].str.replace('False', '')

data = data[data['Country'].isin(['United States', 'Australia', 'New Zealand'])]

data.to_csv('data_cleaned.csv', index=False)
