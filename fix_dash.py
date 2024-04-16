import pandas as pd

def split_prices(row):
    row['sqft'] = row['sqft'].strip().replace('sqft', '')
    row['bathrooms'] = row['bathrooms'].strip().replace('ba','')
    if '-' in row['price']:
        prices = row['price'].split('-')
        lower_price = prices[0].strip().replace('$', '').replace(',', '')
        higher_price = prices[1].strip().replace('$', '').replace(',', '')

    
        if '-' in row['rooms']:
            rooms = row['rooms'].split('-')
            sqft = row['sqft'].split('-')
            if rooms[0] == 'Studio':
                rooms[0] = 0

            if rooms[1][0] == ' ':
                rooms[1] = chr(ord(rooms[1][1]))
            else:
                rooms[1] = chr(ord(rooms[1][0]))
            
            if '-' in row['bathrooms']:
                bath = row['bathrooms'].split('-')
            
            else:
                bath = {}
                bath[0] = row['bathrooms']
        
            bed_range = range(int(rooms[0]), int(rooms[1]) + 1)
            
            for bed in bed_range:
                new_row = row.copy()
                new_row['price'] = lower_price if bed == bed_range[0] else higher_price
                if len(sqft) > 1: 
                    new_row['sqft'] = sqft[0] if bed == bed_range[0] else sqft[1]
                else:
                    new_row['sqft'] = sqft[0]
                if len(bath) > 1:
                    new_row['bathrooms'] = bath[0] if bed == bed_range[0] else bath[1]
                else:
                    new_row['bathrooms'] = bath[0] 


                new_row['rooms'] = bed
                yield new_row
        else:
            index = 0
            for price in prices:
                new_row = row.copy()
                new_row['price'] = lower_price if index == 0 else higher_price
                new_row['rooms'] = row['rooms']
                index+=1
                yield new_row
    else:
        yield row

def add_city(file_path):
    df = pd.read_csv(file_path)
    df = df[~(df == '—').any(axis=1)]
    df = df[~(df == '— beds').any(axis=1)]
    df['rooms'] = df['rooms'].str.replace(' beds', '').str.replace(' bed', '')
    df['bathrooms'] = df['bathrooms'].str.replace(' beds', '').str.replace(' bed', '')
    df['sqft'] = df['sqft'].str.replace(',', '')
    df['rent'] = df['rent'].str.replace(',', '').str.replace('$', '')

    for index, row in df.iterrows():
        if float(row['sqft']) < 1:
            df.at[index, 'sqft'] = str(round(float(row['sqft']) * 43560, 1))

    return df

    #df['rooms'] = df['rooms'].str.replace(r'\s+', '', regex=True).str.replace('beds', '')
    #df['bathrooms'] = df['bathrooms'].str.replace(r'\s+', '', regex=True)
    #df['sqft'] = df['sqft'].str.replace(r'\s+', '', regex=True).str.replace(',', '')

    # for index, row in df.iterrows():
    #     yield from split_prices(row)

if __name__ == "__main__":
    file_path = './total/redfin_combined.csv'
    modified_df = pd.DataFrame(add_city(file_path))
    # for index, row in modified_df.iterrows():
    #     if 'Beds' in row['rooms']:
    #         row['rooms'] = chr(ord(row['rooms'][0]))
    
    # if (modified_df['price'] == 'Call for Rent').any():
    #     modified_df = modified_df[modified_df['price'] != 'Call for Rent']
    
    # # Remove "$" and "," characters from the "price" column
    # modified_df['price'] = modified_df['price'].str.replace('$', '').str.replace(',', '').str.replace(' ', '').str.replace('/mo', '')

    modified_df.to_csv('./new_redfin.csv', index=False)