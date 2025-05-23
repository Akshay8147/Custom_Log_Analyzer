import Assessment as pd
import re

# log file path
logname = r"C:\Users\AKKUMARC\Downloads\Logs\1\1.log"

# Define the pattern to remove text up to the first comma or colon
pattern = re.compile(r'^[^,:]*[,:]\s*')

# Initialized an empty list to store log data
log_data = []

# Read the log file
try:
    with open(logname, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Parse the log line using regex
            log_pattern = re.compile(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) (?P<process>[\w\.]+)\[\d+:\d+\]: (?P<component>\w+)\s+(?P<level>[A-Z]) (?P<message>.+)$')
            match = log_pattern.match(line)
            if match:
                log_data.append(match.groupdict())
except Exception as e:
    print(f"Error reading the log file: {e}")

# Converting the log data to a DataFrame
df = pd.DataFrame(log_data)

# Applying pattern to the 'message' column to clean it
df['message_cleaned'] = df['message'].apply(lambda x: pattern.sub('', x))

# Exporting the DataFrame to an Excel file
output_filename = "cleaned_log_data.xlsx"
df.to_excel(output_filename, index=False, sheet_name='LogData')

print(f"Cleaned data has been written to {output_filename}")