import os
import csv

# Directory containing your TXT files
txt_dir = 'data/instances3'
# Output CSV file name
# Output CSV file name
output_csv = 'instances3.csv'

# List to store rows of data
data_rows = []

# Function to extract vehicle number and capacity
def extract_vehicle_info(file_path):
    vehicle_info = {}
    vehicles = False
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            parts = line.split()
            if vehicles:
                if len(parts) == 2:
                    num_vehicles = int(parts[0])
                    capacity = int(parts[1])
                    vehicle_info["Number of Vehicles"] = num_vehicles
                    vehicle_info["Capacity"] = capacity
                    vehicles = False
                    break
            if line.startswith("NUMBER"):
                vehicles = True
    return vehicle_info


# List to store rows of data
data_rows = []

# Iterate through the TXT files in the directory
for filename in os.listdir(txt_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(txt_dir, filename)

        # Extract vehicle information
        vehicle_data = extract_vehicle_info(file_path)
        num_vehicles = vehicle_data.get("Number of Vehicles", "")
        capacity = vehicle_data.get("Capacity", "")

        # Read customer data
        with open(file_path, 'r') as txt_file:
            lines = txt_file.readlines()

            # Remove empty lines and header lines
            lines = [line for line in lines if
                     line.strip() and not line.startswith("CUSTOMER") and not line.startswith("CUST NO.")]

            # Create a row for the CSV file

            row = [filename, len(lines)-5, num_vehicles, capacity]

            for i, line in enumerate(lines[1:], start=1):  # Skip the first line
                customer = line.split()
                if len(customer) >= 3:
                    row += customer[1:]
                    #for value in customer:
                        #row += ''.join(filter(str.isdigit, value))
                        #print(value)
                    print(customer[1:7])
                    print(row)

            # Append the row to the data_rows list
            data_rows.append(row)

# Create headers for the CSV file
headers = ['Filename', 'Customer Count', 'Number', 'Capacity']
headers += ['x_depot', 'y_depot', 'demand_depot', 'ready_depot', 'due_depot', 'service_depot']
for i in range(1,51):
    headers += [f'x_{i}']
    headers += [f'y_{i}']
    headers += [f'demand_{i}']
    headers += [f'ready_{i}']
    headers += [f'due_{i}']
    headers += [f'service_{i}']

# Write data to CSV file
with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)
    csv_writer.writerows(data_rows)

print(f'Data written to {output_csv}')