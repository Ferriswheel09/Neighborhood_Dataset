import pandas as pd
file_path = './total/apartments_combined.csv'


modified_df = pd.read_csv(file_path)

city_state_zip = modified_df['address'].str.split(',').str[-2:]

# Extract city, state, and zipcode
modified_df['city'] = city_state_zip.str[0]
modified_df['state_zipcode'] = city_state_zip.str[1]

# Remove leading/trailing whitespace from the "city" and "state_zipcode" columns
modified_df['city'] = modified_df['city'].str.strip()
modified_df['state_zipcode'] = modified_df['state_zipcode'].str.strip()

# Append state abbreviation to city
modified_df['city'] = modified_df['city'] + ', ' + modified_df['state_zipcode'].str[:2]

# Remove the state abbreviation and zip code from the "state_zipcode" column
modified_df.drop(columns=['state_zipcode'], inplace=True)

modified_df.to_csv(file_path, index=False)