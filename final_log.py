import Assessment as pd
import re
import os

# Path to the log file
logname = r"C:\Users\AKKUMARC\Downloads\Logs\1\1.log"

# Start and end markers as regular expressions
start_marker = re.compile(r'^Apr 10 11:15:32\.104831')
end_marker = re.compile(r'^Apr 10 11:15:32\.122577')

# Read the log file between the markers
log_lines = []
within_section = False
with open(logname, 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        if start_marker.match(line.strip()):
            within_section = True
        if within_section:
            log_lines.append(line)
        if end_marker.match(line.strip()):
            within_section = False
            break

# Remove text until comma or colon is found
for i in range(len(log_lines)):
    log_lines[i] = re.sub(r'^.*?[,:]', '', log_lines[i])

# Exclude lines containing a particular string
exclude_string = "ForwardingEngine"
log_lines_filtered = [line for line in log_lines if exclude_string not in line]

# Search lines containing a specific text
search_text = "ForwardingEngine"
searched_lines = [line for line in log_lines if search_text in line]

# Write searched lines to a separate output file
output_search_file = "output_searched.txt"
with open(output_search_file, 'w', encoding='utf-8') as file:
    file.writelines(searched_lines)

# Generate an output text file for lines with removed text until comma or colon
output_removed_text_file = "output_removed_text.txt"
with open(output_removed_text_file, 'w', encoding='utf-8') as file:
    file.writelines(log_lines)

# Generate an output text file for lines excluding a particular string
output_excluded_string_file = "output_excluded_string.txt"
with open(output_excluded_string_file, 'w', encoding='utf-8') as file:
    file.writelines(log_lines_filtered)

# Convert log lines to DataFrame for further processing if needed
log_data = []
for line in log_lines:
    match = re.match(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) (?P<process>[\w\.]+)\[\d+:\d+\]: (?P<component>\w+)\s+(?P<level>[A-Z]) (?P<message>.+)$', line.strip())
    if match:
        log_data.append(match.groupdict())

df = pd.DataFrame(log_data)

# Generate an output excel sheet for the filtered data
output_filtered_file = "output_filtered.xlsx"
if os.path.exists(output_filtered_file):
    os.remove(output_filtered_file)

df.to_excel(output_filtered_file, sheet_name="Filtered_Data", index=False)

# Display the DataFrame
print(df.head())
