import Assessment as pd
import sys
import os

def parse_logs(log_dir_path, output_file_path, start_log=None, end_log=None, start_line=None, end_line=None):
    log_entries = []

    def process_file(file_path, start_line=None, end_line=None):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start_index = int(start_line) - 1 if start_line else 0
            end_index = int(end_line) if end_line else len(lines)

            for line in lines[start_index:end_index]:
                log_entries.append({"line": line.strip()})

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
        df.to_excel(output_file_path, index=False)
        print(f"Filtered data has been saved to {output_file_path}")
    else:
        print("No log entries found.")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python final_log_parser.py <log_directory_or_file> <output_file> [<start_log>] [<end_log>] <start_line> <end_line>")
    else:
        log_dir_path = sys.argv[1]
        output_file_path = sys.argv[2]
        start_log = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].isdigit() else None
        end_log = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].isdigit() else None
        start_line = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5].isdigit() else None
        end_line = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6].isdigit() else None

        parse_logs(log_dir_path, output_file_path, start_log, end_log, start_line, end_line)
