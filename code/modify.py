import os
import json
import jsonschema
from datetime import datetime

# Update the file paths below or it won't work.

# New function to write errors to a file
def write_error_to_file(error_message):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_file_name = f"error_log_{timestamp}.txt"
    with open(error_file_name, 'a', encoding='utf-8') as error_file:
        error_file.write(f"{datetime.now()}: {error_message}\n\n")

def replace_min_max(item):
    if isinstance(item, dict):
        if 'ClassName' in item and 'ammo' in item['ClassName'].lower() and 'box' not in item['ClassName'].lower():
            if 'Quantity' in item:
                if 'Min' in item['Quantity']:
                    item['Quantity']['Min'] = 0.3
                if 'Max' in item['Quantity']:
                    item['Quantity']['Max'] = 0.5
        for key, value in item.items():
            replace_min_max(value)
    elif isinstance(item, list):
        for element in item:
            replace_min_max(element)

def add_new_ammo_entries(item):
    new_entries = [
        {
            "ClassName": "Ammo_308Win",
            "Chance": 0.65,
            "Quantity": {
                "Min": 0.3,
                "Max": 0.6
            },
            "Health": [
                {
                    "Min": 1.0,
                    "Max": 1.0,
                    "Zone": ""
                }
            ]
        },
        {
            "ClassName": "AmmoBox_308Win_20Rnd",
            "Chance": 0.33,
            "Quantity": {
                "Min": 0.0,
                "Max": 0.0
            },
            "Health": [
                {
                    "Min": 1.0,
                    "Max": 1.0
                }
            ]
        }
    ]

    def find_and_add_ammo_entries(data):
        if isinstance(data, list):
            if any('ClassName' in elem and ('ammo' in elem['ClassName'].lower() or 'ammobox' in elem['ClassName'].lower()) for elem in data):
                data.extend(new_entries)
            else:
                for element in data:
                    find_and_add_ammo_entries(element)
        elif isinstance(data, dict):
            for key, value in data.items():
                find_and_add_ammo_entries(value)

    find_and_add_ammo_entries(item)

def validate_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
        
        # Basic schema for DayZ loadout files
        schema = {
            "type": "object",
            "required": ["ClassName", "Chance", "Quantity", "Health", "InventoryAttachments", "InventoryCargo", "Sets"],
            "properties": {
                "ClassName": {"type": "string"},
                "Chance": {"type": "number"},
                "Quantity": {
                    "type": "object",
                    "properties": {
                        "Min": {"type": "number"},
                        "Max": {"type": "number"}
                    }
                },
                "Health": {"type": "array"},
                "InventoryAttachments": {"type": "array"},
                "InventoryCargo": {"type": "array"},
                "Sets": {"type": "array"}
            }
        }
        
        jsonschema.validate(instance=content, schema=schema)
        print(f"Validation successful: {file_path}")
        return True
    except json.JSONDecodeError as e:
        error_message = f"JSON Decode Error in {file_path}: {str(e)}"
        print(error_message)
        write_error_to_file(error_message)
        return False
    except jsonschema.exceptions.ValidationError as e:
        error_message = f"Schema Validation Error in {file_path}: {str(e)}"
        print(error_message)
        write_error_to_file(error_message)
        return False
    except Exception as e:
        error_message = f"Unexpected error during validation of {file_path}: {str(e)}"
        print(error_message)
        write_error_to_file(error_message)
        return False

def process_multiple_files(input_directory, output_directory, process_functions):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for root, _, filenames in os.walk(input_directory):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                
                # Determine new file path
                relative_path = os.path.relpath(root, input_directory)
                new_directory = os.path.join(output_directory, relative_path)
                if not os.path.exists(new_directory):
                    os.makedirs(new_directory)
                
                new_file_path = os.path.join(new_directory, filename)
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)

                for func in process_functions:
                    func(content)

                with open(new_file_path, 'w', encoding='utf-8') as file:
                    json.dump(content, file, indent=4)
                
                print(f"Processed file: {new_file_path}")
                
                # Validate the output file
                if not validate_json(new_file_path):
                    print(f"Warning: Validation failed for {new_file_path}")

# Configuration
input_directory = r"C:\Users\andre\OneDrive\Documents\DayZ Loadouts\modify\input"
output_directory = r"C:\Users\andre\OneDrive\Documents\DayZ Loadouts\modify\output"

# Set these flags to True for the operations you want to perform
do_replace_min_max = False
do_add_new_ammo_entries = True

# Create a list of functions to apply based on the flags
process_functions = []
if do_replace_min_max:
    process_functions.append(replace_min_max)
if do_add_new_ammo_entries:
    process_functions.append(add_new_ammo_entries)

# Run the processing
process_multiple_files(input_directory, output_directory, process_functions)