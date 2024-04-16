import csv
import os

def combine_csv(str):
    files = os.listdir(str)

    combined_rows = []

    for i, file_name in enumerate(files):
        file_path = os.path.join(str, file_name)
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            
            for j, row in enumerate(reader):
                if i != 0 and j == 0:
                    continue
                
                combined_rows.append(row)


    output_file_path = os.path.join(str, "output.csv")

    with open(output_file_path, "w", newline='') as output_file:
        writer = csv.writer(output_file)
        for row in combined_rows:
            writer.writerow(row) 

    print("Combined CSV file created successfully at:", output_file_path)


if __name__ == "__main__":
    path = "./final_compilation"
    #path = "./apartments/by_city"
    combine_csv(path)
