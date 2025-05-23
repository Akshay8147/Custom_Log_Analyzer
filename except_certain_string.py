import Assessment as pd
import re

# pattern to remove string
log_pattern = re.compile(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) (?P<process>[\w\.]+)\[\d+:\d+\]: (?P<component>\w+)\s+(?P<level>[A-Z]) (?P<message>.+)$')

# log file path
logname = r"C:\Users\AKKUMARC\Downloads\Logs\1\1.log"

# String to exclude lines containing certain text
exclude_string = 'ForwardingEngine'

# lists to store the log components
timestamps, processes, components, levels, messages = [], [], [], [], []

# Read the log file
with open(logname, 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        match = log_pattern.match(line)
        if match:
            timestamps.append(match.group('timestamp'))
            processes.append(match.group('process'))
            components.append(match.group('component'))
            levels.append(match.group('level'))
            messages.append(match.group('message'))

# Creating DataFrame from the parsed log data
data = {
    'timestamp': timestamps,
    'process': processes,
    'component': components,
    'level': levels,
    'message': messages
}

df = pd.DataFrame(data)

# Filtering the DataFrame to exclude lines containing the specific string
filtered_df = df[~df['component'].str.contains(exclude_string, case=False, na=False)]

# Display the filtered DataFrame
print(filtered_df)

# Exporting the filtered DataFrame to an Excel file
output_filename = "filtered_log_data.xlsx"
filtered_df.to_excel(output_filename, index=False, sheet_name='LogData')

print(f"Filtered data has been written to {output_filename}")
