import csv
import os

def combine_csv(directory):
    files = os.listdir(directory)

    combined_rows = []
    header_written = False

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            if not header_written:
                # Write the header from the first file
                header = next(reader)
                header.append("apartment_or_house")
                combined_rows.append(header)
                header_written = True
            
            for row in reader:
                # Add the type (house/apartment) based on the file name
                if "redfin" in file_name:
                    row.append("house")
                elif "newer_apartments" in file_name:
                    row.append("apartment")
                
                combined_rows.append(row)

    # Specify the order of columns
    columns_order = ["city", "address", "price", "rooms", "bathrooms", "sqft", "apartment_or_house"]

    output_file_path = os.path.join(directory, "output3.csv")

    with open(output_file_path, "w", newline='') as output_file:
        writer = csv.writer(output_file)
        # Write header with specified column order
        writer.writerow(columns_order)
        # Write rows
        for row in combined_rows:
            writer.writerow(row) 

    print("Combined CSV file created successfully at:", output_file_path)


if __name__ == "__main__":
    directory_path = "./final_compilation"
    combine_csv(directory_path)
