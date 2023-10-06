import csv
import os

# Function to read data from a CSV file and return it as a list of dictionaries
def read_csv_to_list(filename, delimiter=','):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            data.append(row)
    return data

# Function to combine data from two CSV files by matching values in different fields
def combine_csv_files(file1, file2, field1, field2):
    # Read data from both CSV files
    data1 = read_csv_to_list(file1, delimiter=';')
    data2 = read_csv_to_list(file2)

    # Combine data based on the common field values
    combined_data = []

    # Create a mapping between the field values
    mapping = {os.path.splitext(row[field2])[0]: row for row in data2}

    # Iterate through data1 and find matching rows in data2
    for row1 in data1:
        if field1 in row1:
            value1 = os.path.splitext(row1[field1])[0]
            matching_row = None

            # Find the matching row in data2 based on field2
            for row2 in data2:
                if field2 in row2 and os.path.splitext(row2[field2])[0] == value1:
                    matching_row = row2
                    break

            if matching_row:
                combined_row = {**row1, **matching_row}
                combined_data.append(combined_row)

# Define the filenames and field names
file1 = 'modified_solution.csv'
file2 = 'instances.csv'
field1 = 'inst_name'  # Field name in file2
field2 = 'Filename'  # Field name in file1



# Combine the CSV files
combined_data = combine_csv_files(file1, file2, field1, field2)

# Define the output CSV filename
output_file = 'combined_output.csv'

if combined_data:
    # Write the combined data to a new CSV file
    with open(output_file, mode='w', newline='') as file:
        fieldnames = combined_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

    print(f"Combined data saved to {output_file}")
else:
    print("No matching data found between the two CSV files.")





