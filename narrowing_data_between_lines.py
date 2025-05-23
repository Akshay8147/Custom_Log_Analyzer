import re
import Assessment as pd

# Regular expression pattern
log_pattern = re.compile(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) (?P<process>[\w\.]+)\[\d+:\d+\]: (?P<component>\w+)\s+(?P<level>[A-Z]) (?P<message>.+)$')

# Patterns for start and end lines
start_pattern = re.compile(r'^Apr 10 11:15:32\.104831')
end_pattern = re.compile(r'^Apr 10 11:15:32\.122577')

# log file path
logname = r"C:\Users\AKKUMARC\Downloads\Logs\1\1.log"

# Read the log file and extract lines between the start and end patterns
extracting = False
data = []

with open(logname, 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        if start_pattern.match(line):
            extracting = True
        if extracting:
            match = log_pattern.match(line)
            if match:
                data.append(match.groupdict())
        if end_pattern.match(line):
            extracting = False
            break

# Creating a DataFrame from the extracted data
df = pd.DataFrame(data)


print(df)

# Exporting the DataFrame to an Excel file
output_filename = "extracted_log_data.xlsx"
df.to_excel(output_filename, index=False, sheet_name='LogData')

print(f"Extracted data has been written to {output_filename}")
