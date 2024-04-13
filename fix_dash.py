import pandas as pd

def split_prices(row):
    if '-' in row['price']:
        prices = row['price'].split('-')
        lower_price = prices[0].strip().replace('$', '').replace(',', '')
        higher_price = prices[1].strip().replace('$', '').replace(',', '')

    
        if '-' in row['rooms']:
            rooms = row['rooms'].split('-')

            if type(rooms[0]) is str:
                rooms[0] = 0

            if rooms[1][0] == ' ':
                rooms[1] = chr(ord(rooms[1][1]))
            else:
                rooms[1] = chr(ord(rooms[1][0]))
        
            bed_range = range(int(rooms[0]), int(rooms[1]) + 1)
            
            for bed in bed_range:
                new_row = row.copy()
                new_row['price'] = lower_price if bed == bed_range[0] else higher_price
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
    
    for index, row in df.iterrows():
        yield from split_prices(row)

if __name__ == "__main__":
    file_path = './total/apartments_combined.csv'
    modified_df = pd.DataFrame(add_city(file_path))
    for index, row in modified_df.iterrows():
        if 'Beds' in row['rooms']:
            row['rooms'] = chr(ord(row['rooms'][0]))
    
    if (modified_df['price'] == 'Call for Rent').any():
        modified_df = modified_df[modified_df['price'] != 'Call for Rent']
    
    # Remove "$" and "," characters from the "price" column
    modified_df['price'] = modified_df['price'].str.replace('$', '').str.replace(',', '').str.replace(' ', '').str.replace('/mo', '')

    modified_df.to_csv(file_path, index=False)