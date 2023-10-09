import pandas as pd

# Specify the file paths for your CSV files
file1_path = '../modified_data/modified_solution.csv'
file2_path = '../modified_data/instances.csv'

# Read the CSV files into dataframes
df_solution = pd.read_csv(file1_path, sep=';')
df_instances = pd.read_csv(file2_path)

df_instances['Filename'] = df_instances['Filename'].str.replace('.txt', '')

merged_df = pd.merge(df_solution, df_instances, left_on='inst_name', right_on='Filename', how='inner')

print(0)

# Now, df1 and df2 contain the data from your CSV files in separate dataframes
