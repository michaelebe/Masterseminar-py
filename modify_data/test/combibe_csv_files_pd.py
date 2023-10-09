import pandas as pd

# Define the filenames
file1 = 'modified_solution.csv'
file2 = 'instances.csv'

# Read the CSV files into pandas DataFrames
df1 = pd.read_csv(file1, delimiter=';')
df2 = pd.read_csv(file2)

# Define the mapping between field1 and field2 values
field1 = 'inst_name'
field2 = 'Filename'

# Read the CSV files into pandas DataFrames
df1 = pd.read_csv(file1, delimiter=';')
df2 = pd.read_csv(file2)

# Remove the file extension from field1 to match field2
df1[field1] = df1[field1].str.replace('.txt', '')

# Merge the DataFrames based on the common field
combined_data = df1.merge(df2, left_on=field1, right_on=field2, how='inner')

# Define the output CSV filename
output_file = 'combined_output.csv'

# Save the combined data to a new CSV file
combined_data.to_csv(output_file, index=False)

print(f"Combined data saved to {output_file}")