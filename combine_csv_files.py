import csv
import os

# Function to read data from a CSV file and return it as a list of dictionaries
def read_csv_to_list(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to combine data from two CSV files by matching values in different fields
def combine_csv_files(file1, file2, field1, field2):
    # Read data from both CSV files
    data1 = read_csv_to_list(file1)
    data2 = read_csv_to_list(file2)

    # Create a mapping between the field values
    mapping = {os.path.splitext(row[field2])[0]: row for row in data2}

    # Combine data based on the common field values
    combined_data = []
    for row1 in data1:
        value1 = os.path.splitext(row1[field1])[0]
        if value1 in mapping:
            combined_row = {**row1, **mapping[value1]}
            combined_data.append(combined_row)

    return combined_data

# Define the filenames and field names
file1 = 'instances.csv'
file2 = 'modified_solution.csv'
field1 = 'Filename'  # Field name in file1
field2 = 'inst_name'  # Field name in file2


# Combine the CSV files
combined_data = combine_csv_files(file1, file2, field1, field2)

# Define the output CSV filename
output_file = 'combined_output.csv'

# Write the combined data to a new CSV file
with open(output_file, mode='w', newline='') as file:
    fieldnames = combined_data[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)

print(f"Combined data saved to {output_file}")