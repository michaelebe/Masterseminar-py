import csv
import re


# Function to convert a route string to a list of integers
def convert_route(route_str):
    # Use regular expressions to extract numbers within parentheses
    route_parts = re.findall(r'\((.*?)\)', route_str)

    # Convert the extracted numbers to integers
    route_list = [int(num) for part in route_parts for num in part.split()]

    return route_list


# Function to convert a cuts string to a list of tuples
def convert_cuts(cuts_str):
    # Use regular expressions to find and extract lmSR and Memory parts
    lmSR_parts = re.findall(r'lmSR: \((.*?)\)', cuts_str)
    memory_parts = re.findall(r'Memory: \((.*?)\)', cuts_str)

    # Initialize lists to store the converted data
    cuts_tuples = []

    # Process lmSR and Memory parts together
    for lmSR, memory in zip(lmSR_parts, memory_parts):
        lmSR_list = list(map(int, lmSR.split()))
        # Split the memory part and filter out empty strings
        memory_list = [int(num) for num in memory.split(',') if num]

        # Combine lmSR and Memory lists into tuples and append to the result
        cuts_tuples.append((lmSR_list, memory_list))

    return cuts_tuples

# Function to extract pi values from the dual_variables field
def extract_pi_values(dual_variables_str):
    pi_values = re.findall(r'pi\((.*?)\)=([\d.]+)', dual_variables_str)
    return [float(value) for (_, value) in pi_values]

# Function to extract sigma_lm values and memory from the dual_variables field
def extract_sigma_lm_and_memory(dual_variables_str):
    sigma_lm_matches = re.findall(r'sigma_lm\((.*?)\) = ([\d.-]+) Memory size: (\d+) \|\| Memory: (.*?)\s*(?=\bsigma_lm\b|$)', dual_variables_str)
    return [(nodes.split(), float(value), int(memory_size), memory.split()) for (nodes, value, memory_size, memory) in sigma_lm_matches]

# Open the original CSV file in read mode
with open('../output_file.csv', mode='r') as input_file:
    # Create a DictReader using the semicolon delimiter
    csv_reader = csv.DictReader(input_file, delimiter=';')

    # Initialize an empty list to store the modified rows
    modified_rows = []

    # Iterate through the rows in the CSV
    for row in csv_reader:
        # Convert the 'routes' field and replace it with the converted list
        row['routes'] = [convert_route(route_str) for route_str in row['routes'].split('),')]

        # Convert the 'cuts' field and replace it with the converted list of tuples
        row['cuts'] = convert_cuts(row['cuts'])

        # Extract pi values and store in the 'dual_variables_nodes' field
        row['dual_variables_nodes'] = extract_pi_values(row['dual_variables'])

        # Extract sigma_lm values and memory and store in the 'dual_variables_cuts' field
        row['dual_variables_cuts(cut, dual value, memory size, memory)'] = extract_sigma_lm_and_memory(row['dual_variables'])

        # Delete the original 'dual_variables' field
        del row['dual_variables']

        # Append the modified row to the list
        modified_rows.append(row)

# Define the list of column names for the output CSV, excluding 'dual_variables'
fieldnames = [name for name in csv_reader.fieldnames if name != 'dual_variables']

# Define the list of column names for the output CSV, including the new fields
fieldnames +=  ['dual_variables_nodes', 'dual_variables_cuts(cut, dual value, memory size, memory)']


# Open a new CSV file in write mode to write the modified content
with open('../modified_data/modified_solution.csv', mode='w', newline='') as output_file:
    # Create a DictWriter with the semicolon delimiter
    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')

    # Write the header row to the new CSV file
    csv_writer.writeheader()

    # Write the modified rows to the new CSV file
    csv_writer.writerows(modified_rows)
