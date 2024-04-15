import os

# List of .py files to execute
file_list = ['add_Mark.py', 'get_price_from_yahoo.py', 'get_industry_from_yahoo.py']

# Iterate over the file list
for file in file_list:
    # Check if the file exists
    if os.path.exists(file):
        # Execute the file using the 'exec' function
        exec(open(file).read())
    else:
        print(f"File '{file}' does not exist.")


