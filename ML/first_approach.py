import csv
import pandas as pd
import json
import ast
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from itertools import combinations
import numpy as np
from keras.utils import to_categorical
from tensorflow.keras.utils import plot_model
import graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



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
            return obj  # Re

file_path = '../modify_data/data_final.csv'
df = pd.read_csv(file_path, sep=',')

cuts = df['cuts']
cuts_string = cuts.to_json(orient='split')
cuts_json = json.loads(cuts_string)
i=0
for item in cuts:
    current_cuts = cuts_json['data'][i]
    nested_lsit_current_cuts = ast.literal_eval(current_cuts)
    double_nested_array_current_cuts = recursively_convert_to_float(nested_lsit_current_cuts)
    cuts_list = list(double_nested_array_current_cuts)
    df['cuts'][i] = cuts_list
    i+=1

print(df)

'''
# Compute the correlation matrix
correlation_matrix = df.corr()
print(correlation_matrix)
# Create a heatmap
plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar(label='Correlation Coefficient')
plt.title('Correlation Heatmap')
plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix)), correlation_matrix.columns)
plt.show()
'''

def remove_second_value(cuts):
    return [cut[0] for cut in cuts]

X = df.drop('cuts', axis=1)
y = df['cuts']
# Apply the function to the 'cuts' column
y = y.apply(remove_second_value)
y_bool = df['cuts'].apply(lambda cuts: bool(cuts))
print(df['cuts'])
print(y_bool)

# Split the data into training and test sets (usually, 70-80% for training and 20-30% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y_bool, test_size=0.3, random_state=42)

# Create a simple neural network model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # For binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the training data
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f'Test Loss: {test_loss:.4f}')
print(f'Test Accuracy: {test_accuracy:.4f}' )

plot_model(model, to_file='model_bool.png', show_shapes=True, show_layer_names=True)

# Create a Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the Random Forest model on the training data
rf_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rf_model.predict(X_test)

# Calculate accuracy on the test data
rf_accuracy = accuracy_score(y_test, y_pred)

print(f'Random Forest Test Accuracy: {rf_accuracy:.4f}')
# Assuming you have already trained your Random Forest model (rf_model)
feature_names = X.columns  # Replace with your actual feature names

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.bar(range(len(rf_model.feature_importances_), rf_model.feature_importances_)
plt.xticks(range(len(feature_names)), feature_names, rotation=90)
plt.xlabel("Features")
plt.ylabel("Feature Importance")
plt.title("Random Forest Feature Importance")
plt.show()

# Create a list of node numbers from 1 to 25
nodes = [float(i) for i in range(1, 26)]
# Generate all combinations of 3 nodes
combinations_3 = list(combinations(nodes, 3))
# Create Boolean columns for each combination
for i, combo in enumerate(combinations_3):
    column_name = f"cut_{combo[0]}_{combo[1]}_{combo[2]}"
    df[column_name] = False

# Print the DataFrame (optional)
print(df.head())

index=0
for item in df['cuts']:
    cuts_curr = item
    for i,combo in enumerate(combinations_3):
        for j in range(0, len(cuts_curr)):
            for l in range(0, len(cuts_curr[j])):
                if combo[0] == cuts_curr[j][l][0]:
                    if combo[1] == cuts_curr[j][l][1]:
                        if combo[2] == cuts_curr[j][l][2]:
                            #print(cuts_curr[j])
                            #print(combo)
                            column_name = f"cut_{combo[0]}_{combo[1]}_{combo[2]}"
                            df[column_name][index] = True
    index+=1


values_to_append = []
X = df.drop('cuts', axis=1)
y = df
for i, combo in enumerate(combinations_3):
    column_name = f"cut_{combo[0]}_{combo[1]}_{combo[2]}"
    X.drop(column_name ,axis=1)
    values_to_append.append(column_name)

y = df[[col for col in df.columns if col in values_to_append]]

print(y)

# Convert boolean values to integers (0 and 1)
y = y.astype(int)
print("Shape of y after conversion:", y.shape)
print("Data type of y after conversion:", y.dtypes)
#y = to_categorical(y, num_classes=2300)
#print("categorical", y)

# Convert X to the correct data type
X = X.astype('float32')


# Split the data into training and test sets (usually, 70-80% for training and 20-30% for testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a simple neural network model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(2300, activation='softmax')  # For binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Train the model on the training data
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)

print(f'Test Loss: {test_loss:.4f}')
print(f'Test Accuracy: {test_accuracy:.4f}' )

# Generate and save the model architecture as an image
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)


