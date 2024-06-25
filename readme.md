# DayZ Loadout JSON Processor

This Python script processes and modifies DayZ loadout JSON files. It can adjust ammo quantities and add new ammo types to existing loadout configurations.

## Features

- Modify minimum and maximum ammo quantities
- Add new 5.45x39 ammo entries to loadout files
- Validate JSON structure of processed files
- Error logging to separate files for easy debugging

## Requirements

- Python 3.6+
- jsonschema library

## Usage

1. Set your input and output directories in the script:
    ```python
    input_directory = r"C:\path\to\your\input\directory"
    output_directory = r"C:\path\to\your\output\directory"
    ```

2. Choose which operations to perform by setting the flags:
    ```python
    do_replace_min_max = False
    do_add_new_ammo_entries = True
    ```

3. Run the script:
    ```bash
    python dayz_loadout_processor.py
    ```

## Functions

- `replace_min_max(item)`: Adjusts the minimum and maximum quantities for ammo items.
- `add_new_ammo_entries(item)`: Adds new 5.45x39 ammo entries to appropriate locations in the loadout.
- `validate_json(file_path)`: Validates the structure of processed JSON files.
- `process_multiple_files(input_directory, output_directory, process_functions)`: Main function that processes all JSON files in the input directory.

## Error Logging

Errors during processing are logged to a file named `error_log_YYYYMMDD_HHMMSS.txt` in the script's directory. Each error message includes a timestamp for easy tracking.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## License

MIT
