import subprocess
import re

def run_flake8("C:/Users/AKKUMARC/PycharmProjects/pythonProject1/input.py"):

    result = subprocess.run(["flake8", "C:/Users/AKKUMARC/PycharmProjects/pythonProject1/input.py"], capture_output=True, text=True)
    return result.stdout.strip().split("\n")

def insert_comments(file_path, issues):

    with open(file_path, "r") as file:
        lines = file.readlines()

    comments = {}
    for issue in issues:
        if not issue:
            continue
        match = re.match(r"(\d+):(\d+): (.+)", issue)
        if match:
            line_no = int(match.group(1)) - 1  # Adjust for zero-based index
            message = match.group(3)
            comments[line_no] = f"  # TODO: {message}"

    formatted_lines = []
    for i, line in enumerate(lines):
        formatted_lines.append(line.rstrip())  # Remove trailing spaces
        if i in comments:
            formatted_lines.append(comments[i])  # Append comment for that line

    with open(f"{file_path}.reviewed", "w") as file:
        file.write("\n".join(formatted_lines) + "\n")

    print(f"Reviewed file saved as {file_path}.reviewed")

if __name__ == "__main__":
    file_to_check = "sample.py"  # Change this to your file name
    issues = run_flake8(file_to_check)
    insert_comments(file_to_check, issues)

