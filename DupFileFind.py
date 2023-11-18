# This script is more robust when dealing with large files and exceptions, and presents the results in a more user-friendly way.

import os
import hashlib
import argparse
import concurrent.futures

# This function is used to calculate the MD5 hash of a file
def calculate_md5(file_path):
    try:
        # Create a new hashlib.md5 object
        hash_md5 = hashlib.md5()
        # Open the file and read its content
        with open(file_path, 'rb') as file:
            # Read the file content in chunks and update the hash
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
        # Return the hash in hexadecimal format
        return hash_md5.hexdigest()
    except Exception as e:
        # If an error occurs while reading the file, print the error message and return None
        print(f"Error reading file {file_path}: {str(e)}")
        return None

# This function is used to find duplicate files in the target directory
def find_duplicates(target_directory):
    # Create a dictionary to store the file hashes and their corresponding file paths
    file_hashes = {}
    # Use the concurrent.futures module to implement multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Traverse the target directory and all its subdirectories
        for dirpath, dirnames, filenames in os.walk(target_directory):
            # Calculate the hash of each file and add it to the future_to_file dictionary
            future_to_file = {executor.submit(calculate_md5, os.path.join(dirpath, filename)): filename for filename in filenames}
            # When a task is completed, get the result and update the file_hashes dictionary
            for future in concurrent.futures.as_completed(future_to_file):
                filename = future_to_file[future]
                file_hash = future.result()
                if file_hash:
                    if file_hash in file_hashes:
                        file_hashes[file_hash].append(filename)
                    else:
                        file_hashes[file_hash] = [filename]
    # Select the hashes that have more than one file path from the dictionary, these are the duplicate files
    duplicates = {k: v for k, v in file_hashes.items() if len(v) > 1}
    return duplicates

# Parse command-line arguments to get the target directory
parser = argparse.ArgumentParser(description='Find duplicate files in a directory.')
parser.add_argument('directory', type=str, help='The target directory.')
args = parser.parse_args()

# Get the target directory
target_directory = args.directory
# Find duplicate files
duplicates = find_duplicates(target_directory)

# Print the information of duplicate files
for hash, file_paths in duplicates.items():
    print(f"Duplicate files for hash {hash}:")
    for file_path in file_paths:
        print(f"\t{file_path}")

# Print the completion message
print(f"Scan completed. Found {len(duplicates)} duplicate hashes.")
