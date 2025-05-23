import Assessment as pd
import openpyxl
import re
import os

# Enter the pattern to count the occurences by each day
my_pattern_input = "DSWP"
# my_pattern_input = "MIC"
my_pattern = str(my_pattern_input) + "\s*\S*\w*\W*\d*\D*"
#my_pattern = "ForwardingEngine" + "\s*\S*"
# my_pattern = r"MIC\s*\S*"
# my_pattern = "MIC(3/0)link9SFPreceivepowerlowalarmcleared"

# logname = r"C:\Users\tachuth\Desktop\DS_Theertha\BRTJ00_syslog_2022_05_20_14_28_49.log"
# Tz-aware datetime.datetime cannot be converted to datetime64 unless utc=True
# logname = r"C:\Users\tachuth\Desktop\DS_Theertha\BRMJ01_syslog_2022_05_20_14_26_43.log"
# Tz-aware datetime.datetime cannot be converted to datetime64 unless utc=True
logname = r"C:\Users\AKKUMARC\Downloads\Logs\1\1.log"
# Fine with UTC false
# subset = [1,11,12,13,14,15,16,17,18,19,20]
usecols = [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17]
usecols_ = usecols
while usecols_:
    try:
        dataframe = pd.read_table(logname,
                                  delimiter=' ',
                                  low_memory=False,
                                  encoding='unicode_escape',
                                  on_bad_lines='skip',
                                  usecols=usecols_,
                                  # usecols=lambda x: x in subset,
                                  # usecols=[1,11,12,13,14,15,16,17,18,19],
                                  header=None)
        break
    except ValueError as e:
        r = re.search(r"\[(.+)\]", str(e))
        missing_cols = r.group(1).replace("'", "").replace(" ", "").split(",")
        usecols_ = [x for x in usecols_ if x not in missing_cols]

dataframe = pd.read_table(logname,
                          delimiter=' ',
                          low_memory=False,
                          encoding='unicode_escape',
                          on_bad_lines='skip',
                          usecols=usecols_,
                          # usecols=lambda x: x in subset,
                          header=None)

print(dataframe)
columns_name = dataframe.columns.values.tolist()
print(columns_name)
dataframe[0] = pd.to_datetime(dataframe[0], format='%m %d %H:%M:%S', utc=True, errors='coerce')
dataframe[0] = dataframe[0].dt.strftime('%m %d')
# Display the count of rows and columns imported
rows, columns = dataframe.shape
print(rows)
print(columns)
# Concatinate Error Details columns as Detail column
# columns_name=dataframe.columns.values.tolist()
# cols = [x for x in range(12, len(columns_name))]
# print(cols)
cols = [12, 13, 14, 15, 16, 17]
dataframe['Error Details'] = dataframe[cols].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
# Column Formatting
dataframe.rename(columns={1: 'Date', 4: 'Component'}, inplace=True)
print(dataframe)
# df = dataframe.loc[dataframe['Error Details'].str.contains(my_pattern, case=False)]
df = dataframe.loc[dataframe['Error Details'].str.contains(pat=my_pattern, regex=True)]
# displaydataframe
print(df)
rows, columns = df.shape
print(rows)
print(columns)
print(df)
rows = len(dataframe)
assert rows != 0, "No match pattern found !!"
# Create a Dataframe with Date, ErrorComponent, Error Details
Data_ins2 = df[['Date', 'Component', 'Error Details']].value_counts(dropna=False).to_frame()
Data_ins2.rename(columns={0: 'Count'}, inplace=True)
print(Data_ins2.head(60))
# Sort the dataframe based on emerging Date
Data_ins2.sort_values(by='Date', inplace=True)
print(Data_ins2.head(60))
# Generate a output excel sheet
if os.path.exists("output.xlsx"):
    os.remove("output.xlsx")
Data_ins2.to_excel("output.xlsx", sheet_name=str(my_pattern_input))
