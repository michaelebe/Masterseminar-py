import pandas as pd

# Specify the file paths for your CSV files
#mac
#file1_path = '../modified_data/modified_solution.csv'
#file2_path = '../modified_data/instances.csv'

#win
file1_path = 'solution3_modified.csv'
file2_path = 'instances3.csv'



# Read the CSV files into dataframes
df_solution = pd.read_csv(file1_path, sep=';')
df_instances = pd.read_csv(file2_path, sep=',', header=0)

df_instances['Filename'] = df_instances['Filename'].str.replace('.txt', '')

df_solution = df_solution.rename(columns={'inst_name': 'ID'})
df_instances = df_instances.rename(columns={'Filename': 'ID'})

#merged_df = pd.merge(df_solution, df_instances, left_on='ID', right_on='ID', how='outer')
merged_df = pd.merge(df_solution, df_instances, on='ID')

merged_df.to_csv('merged_data3.csv', index=False)


print(df_instances['ID'])
print(df_solution['ID'])

