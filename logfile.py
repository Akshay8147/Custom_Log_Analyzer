import re
import Assessment as pd
import sys
import os

def parse_logs(log_dir_path, keywords, output_file_path, start_log=None, end_log=None, start_line=None, end_line=None):
    log_pattern = re.compile(r'^(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6}) DSWP\.out\[(?P<pid>\d+):(?P<tid>\d+)\]: (?P<module>\w+) +(?P<level>[A-Z]) (?P<message>.+)$')
    log_entries = []

    def process_file(file_path, start_line=None, end_line=None):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start_index = int(start_line) - 1 if start_line else 0
            end_index = int(end_line) if end_line else len(lines)
            for line in lines[start_index:end_index]:
                match = log_pattern.match(line)
                if match:
                    log_entry = match.groupdict()
                    # Convert keywords to strings and check for matches in both 'module' and 'message'
                    if any(str(keyword) in log_entry['module'] or str(keyword) in log_entry['message'] for keyword in keywords):
                        log_entries.append(log_entry)

    # Determine if we're processing a directory or a single file
    if os.path.isdir(log_dir_path):
        log_files = sorted([os.path.join(log_dir_path, f) for f in os.listdir(log_dir_path) if f.endswith(".log")])
        if start_log:
            start_index = next((i for i, f in enumerate(log_files) if os.path.basename(f) == start_log), 0)
        else:
            start_index = 0
        if end_log:
            end_index = next((i for i, f in enumerate(log_files) if os.path.basename(f) == end_log), len(log_files) - 1)
        else:
            end_index = len(log_files) - 1

        for log_file in log_files[start_index:end_index + 1]:
            process_file(log_file, start_line, end_line)
    else:
        process_file(log_dir_path, start_line, end_line)

    if log_entries:
        df = pd.DataFrame(log_entries)
        df.columns = ['timestamp', '1', '2', '3', '4', '5']
        df.to_excel(output_file_path, index=False)
        print(f"Filtered data has been saved to {output_file_path}")
    else:
        print("No log entries found.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python final_log_parser.py <log_directory_or_file> <keywords> <output_file> [<start_log>] [<end_log>] [<start_line>] [<end_line>]")
    else:
        log_dir_path = sys.argv[1]
        keywords = sys.argv[2].split(',')
        output_file_path = sys.argv[3]
        start_log = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].isdigit() else None
        end_log = sys.argv[5] if len(sys.argv) > 5 and not sys.argv[5].isdigit() else None

        # Use safe indexing with default values
        start_line = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6].isdigit() else None
        end_line = sys.argv[7] if len(sys.argv) > 7 and sys.argv[7].isdigit() else None

        parse_logs(log_dir_path, keywords, output_file_path, start_log, end_log, start_line, end_line)
