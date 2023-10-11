import csv
import pandas as pd
import json
import ast

def recursively_convert_to_float(obj):
    if isinstance(obj, list):
        return [recursively_convert_to_float(item) for item in obj]
    elif isinstance(obj, tuple):
        # If it's a tuple, convert its elements to float
        return tuple(recursively_convert_to_float(item) for item in obj)
    else:
        try:
            return float(obj)
        except ValueError:
            return obj  # Return the value as is if it cannot be converted to float

file1_path = 'merged_data3.csv'

# Read the CSV files into dataframes
df_data = pd.read_csv(file1_path, sep=',')

#print(df_data['cuts'])
#print(df_data['dual_variables_cuts(cut, dual value, memory size, memory)'])

dual_values = df_data['dual_variables_cuts(cut, dual value, memory size, memory)']
dual_values_string = dual_values.to_json(orient='split')
dual_values_json = json.loads(dual_values_string)

cuts = df_data['cuts']
cuts_string = cuts.to_json(orient='split')
cuts_json = json.loads(cuts_string)
#for i in range(0,99):
 #   x = dual_values_json['data'][i]
  #  print(type(x))
  #  print(x)


i = 0
redundant_cuts  = []
for item in dual_values_json['data']:
    if item == '[]':
        continue
    else:
        this_dual_value = item[1:-1]
        nested_list = ast.literal_eval(this_dual_value)
        double_nested_array = recursively_convert_to_float(nested_list)
        j = 0
        for item in double_nested_array:
            if item[1] == 0:
                redundant_cuts.append(j)
            j+=1
    current_cuts = cuts_json['data'][i]
    current_cuts = current_cuts[1:-1]
    if current_cuts != '':
        nested_lsit_current_cuts = ast.literal_eval(current_cuts)
        double_nested_array_current_cuts = recursively_convert_to_float(nested_lsit_current_cuts)
        cuts_list = list(double_nested_array_current_cuts)
        #z=1
        #for index in redundant_cuts:
            #cuts_list.pop(index-z-1)
            #z += 1
            #removed_cut = double_nested_array_current_cuts.pop(index)
            #print(removed_cut)

        new_list = [cuts_list[v] for v in range(len(cuts_list)) if v not in redundant_cuts]

    print(df_data['cuts'][i])
    df_data['cuts'][i] = new_list
    print(df_data['cuts'][i])
    i += 1

print(0)



df_data = df_data.drop('dual_variables_cuts(cut, dual value, memory size, memory)', axis=1)
df_data = df_data.drop('dual_variables_nodes', axis=1)
df_data = df_data.drop('host', axis=1)
df_data = df_data.drop('timestamp', axis=1)
df_data = df_data.drop('problem_type', axis=1)
df_data = df_data.drop('ID', axis=1)
df_data = df_data.drop('is_optimal', axis=1)
df_data = df_data.drop('ident', axis=1)
df_data = df_data.drop('info_number_cuts_generations', axis=1)
df_data = df_data.drop('info_num_of_generated_cuts', axis=1)
df_data = df_data.drop('src_limMem', axis=1)
df_data = df_data.drop('maxSRC_LimMem', axis=1)
df_data = df_data.drop('iterationsSRC_limMem', axis=1)
df_data = df_data.drop('customerSRC_limMem', axis=1)
df_data = df_data.drop('customeriterationsSRC_limMem', axis=1)
df_data = df_data.drop('SRC_added_limMem', axis=1)
df_data = df_data.drop('Customer Count', axis=1)
df_data = df_data.drop('inst_class', axis=1)
df_data = df_data.drop('Number', axis=1)
df_data = df_data.drop('routes', axis=1)

df_data.to_csv('data_final.csv', index=False)  # Set index=False to exclude the DataFrame index from the CSV










