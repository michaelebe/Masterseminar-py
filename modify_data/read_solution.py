import csv

# Define the headers as a semicolon-separated string
headers = ["host","timestamp","problem_type","inst_name","inst_class","num_nodes","ident","is_optimal","info_number_cuts_generations"\
    ,"info_num_of_generated_cuts","src_limMem","maxSRC_LimMem","iterationsSRC_limMem","customerSRC_limMem","customeriterationsSRC_limMem"\
    ,"SRC_added_limMem","numVehicles","routes","cuts","dual_variables"]

# Open the original file in read mode
with open('data/solution3.txt', mode='r') as input_file:
    # Read the content of the original file
    lines = input_file.readlines()

# Open a new CSV file in write mode to write the content
with open('solution3.csv', mode='w', newline='') as output_file:
    # Create a CSV writer with a semicolon delimiter
    csv_writer = csv.writer(output_file, delimiter=';')

    # Write the headers to the new CSV file
    csv_writer.writerow(headers)

    # Write the content from the original file
    for line in lines:
        # Split the line using the semicolon delimiter
        values = line.strip().split(';')
        # Write the values to the new CSV file
        csv_writer.writerow(values)