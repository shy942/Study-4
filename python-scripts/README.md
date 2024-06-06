# Python Scripts


## Overview

These scripts facilitate the processing of images from bug reports using the OpenAI API and GPT-4. The workflow consists of several structured steps:

### 1. Extracting Files
If projects are downloaded individually from sources like Google Drive, they often come in ZIP format. Provided is a script that automates the extraction of these ZIP files. It scans a specified directory for ZIP files and extracts their contents to a designated directory where projects are stored, streamlining initial setup.

### 2. Identifying Image Extensions
To determine which files to process, a script analyzes a specified directory and lists all unique file extensions found. This information assists in manually identifying which extensions represent image files.

### 3. Processing Images Through API
Another script is designed for processing multiple projects at a time. To process a project, a corresponding txt file listing the bug reports to be processed is used. Any bug reports not listed are automatically removed from the project. To identify which projects to process, a CSV file is used, formatted as `project_number,txt_title`. Projects listed are processed sequentially. The projects and txt files must be stored in separate, designated directories.

The script used for processing images has global variables which can be modified to adjust arguments sent to the API and which file extensions are used to determine images.



## Requirements


### Software and Libraries:
- **Python**: The scripts require Python 3.7 or later. You can download Python from the [official Python website](https://www.python.org/downloads/).
- **OpenAI Library**: Scripts utilize the OpenAI API for certain functionalities. Install it using pip:
  ```bash
  pip install openai
  ```



## Usage


### 1. Extracting ZIP Files:
- **Script:** `zip_extract_and_organize.py`
- **Command:**
  ```bash
  python zip_extract_and_organize.py /path/to/source/directory /path/to/destination/directory
  ```
  - `/path/to/source/directory`: Path where ZIP files are located.
  - `/path/to/destination/directory`: Path where the extracted files will be stored.

### 2. Printing File Extensions:
- **Script:** `print_file_extensions.py`
- **Command:**
  ```bash
  python print_file_extensions.py /path/to/search/directory
  ```
  - `/path/to/search/directory`: Path where the files have been extracted.

### 3. Processing Images Through an API:
- **Script:** `process_images_with_api.py`
- **Command:**
  ```bash
  python process_images_with_api.py /path/to/directory/for/processing /path/to/directory/with/txts /path/to/csv
  ```
  - `/path/to/directory/for/processing`: Directory where projects are stored.
  - `/path/to/directory/with/txts`: Directory where text files are stored.
  - `/path/to/csv`: Path to CSV file specifying which projects to process and which txt files to use.



