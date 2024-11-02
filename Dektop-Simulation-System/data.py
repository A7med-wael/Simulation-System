import pandas as pd

# Create sample arrival time data
arrival_data = {
    'Time Between Arrivals': [2, 3, 4, 5],
    'Probability': [0.25, 0.40, 0.20, 0.15],
    'Cumulative Probability': [0.25, 0.65, 0.85, 1.00],
    'Digit Assignment From': [1, 26, 66, 86],
    'Digit Assignment To': [25, 65, 85, 100]
}

# Create sample service time data
service_data = {
    'Service Time': [3, 4, 5, 6],
    'Probability': [0.30, 0.28, 0.25, 0.17],
    'Cumulative Probability': [0.30, 0.58, 0.83, 1.00],
    'Digit Assignment From': [1, 31, 59, 84],
    'Digit Assignment To': [30, 58, 83, 100]
}

# Create DataFrames
df_arrivals = pd.DataFrame(arrival_data)
df_service = pd.DataFrame(service_data)

# Combine them into a single DataFrame
# First, rename the columns to avoid conflicts
df_service_renamed = df_service.add_prefix('Service_')
df_combined = pd.concat([df_arrivals, df_service_renamed], axis=1)

# Save to Excel file
df_combined.to_excel('parallel_server_sample_data.xlsx', index=False)

# Display the data
print("Arrival Time Data:")
print(df_arrivals)
print("\nService Time Data:")
print(df_service)