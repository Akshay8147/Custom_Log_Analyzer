import Assessment as pd
import re
import os

# Path to the log file
logname = r"C:\Users\AKKUMARC\Downloads\Logs\2.log"

# Read the log file
with open(logname, 'r', encoding='utf-8', errors='ignore') as file:
    log_lines = file.readlines()

# Define patterns
log_pattern = re.compile(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) (?P<process>[\w\.]+)\[\d+:\d+\]: (?P<component>\w+)\s+(?P<level>[A-Z]) (?P<message>.+)$')

# Parse log lines and store in a list of dictionaries
log_data = []
for line in log_lines:
    match = log_pattern.match(line.strip())
    if match:
        log_data.append(match.groupdict())

# Convert log data to a DataFrame
df = pd.DataFrame(log_data)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%b %d %H:%M:%S.%f', errors='coerce')

# Display the DataFrame
print(df)

# Example of filtering based on the 'ForwardingEngine' pattern
my_pattern_input = "ForwardingEngine"
filtered_df = df[df['component'].str.contains(my_pattern_input, regex=True, case=False)].copy()

# Display the filtered DataFrame
print(filtered_df)

# Count occurrences by date and component, including timestamp
filtered_df['date'] = filtered_df['timestamp'].dt.strftime('%m %d')
result_df = filtered_df.groupby(['date', 'timestamp', 'component']).size().reset_index(name='count')

# Display the result
print(result_df.head(60))

# Generate an output excel sheet
output_file = "output.xlsx"
if os.path.exists(output_file):
    os.remove(output_file)

result_df.to_excel(output_file, sheet_name=str(my_pattern_input), index=False)
