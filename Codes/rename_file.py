import os
import re

# Path to the directory containing the files
directory = 'C:\Users\ashwi\OneDrive\Documents\UMass Amherst\ERSP'

# Regular expression to match files like 'sitting_random123'
pattern = re.compile(r'^sitting_random(\d+)(\.\w+)?$')

for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        number = match.group(1)
        extension = match.group(2) or ''  # in case the file has an extension
        new_filename = f'sitting_still{number}{extension}'
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f'Renamed: {filename} → {new_filename}')
