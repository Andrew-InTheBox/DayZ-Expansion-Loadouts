import os
import csv

def list_json_files(directory):
    # Get a list of all .json files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    return json_files

def write_csv(file_list, output_csv):
    # Write the list of files to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name'])  # Write the header
        for file_name in file_list:
            writer.writerow([file_name])

def main():
    directory = './input'  # Directory to scan for JSON files defined as relative path
    output_csv = './output/loadout_filesnames.csv'  # Output CSV file defined as relative path

    json_files = list_json_files(directory)
    write_csv(json_files, output_csv)
    print(f'CSV file "{output_csv}" created successfully with {len(json_files)} entries.')

if __name__ == '__main__':
    main()