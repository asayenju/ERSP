import os

def truncate_file(file_path):
    """Keep only first 600 lines of a file"""
    temp_path = file_path + '.temp'
    
    try:
        with open(file_path, 'r') as infile, open(temp_path, 'w') as outfile:
            for i, line in enumerate(infile):
                if i < 600:
                    outfile.write(line)
                else:
                    break
        
        os.replace(temp_path, file_path)
        print(f"Truncated {os.path.basename(file_path)} to 600 lines")
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    folder = "./sitting_nodding_diagonal"
    for i in range(1, 76):  # 1-75
        file_path = os.path.join(folder, f"sitting_nod_diagonal{i}.txt")  # Added .txt
        truncate_file(file_path)