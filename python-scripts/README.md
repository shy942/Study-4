# Python Scripts


## Overview

These scripts facilitate the processing of images in bug reports using GPT-4 through the OpenAI API. The workflow consists of several structured steps:

### 1. Extracting Files
If projects are downloaded individually from sources like Google Drive, they often come in ZIP format. Provided is a script that automates the extraction of these ZIP files. It scans a specified directory for ZIP files and extracts their contents to a designated directory where projects are stored, streamlining initial setup.

### 2. Identifying Image Extensions
To determine which files to process, a script analyzes a specified directory and lists all unique file extensions found. This information assisted in the creation of the 3rd script by helping identify which extensions represent image files.

### 3. Processing Images Through API
Another script sequentially processes specified projects, each containing various bug reports and associated images. It identifies the projects to process through a CSV file that matches projects to a txt file listing the bug reports to be processed. Unlisted bug reports within these projects will be deleted, while projects not mentioned in the CSV file will be ignored.



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

### 3. Processing Images with the API:

#### Folder and File Structure

Ensure the following folder structure is maintained for the script to function correctly:

- **`/folder_for_projects/`**
  - **`/project_1/`**, ..., **`/project_n/`:** Each folder represents a specific project.
    - **`/bug_report_1/`**, ..., **`/bug_report_n/`:** Contains files for each bug report.
      - **`image_1.jpg`**, ..., **`image_n.jpg`:** Images associated with the bug report.
- **`/folder_for_txts/`**
  - **`list_for_project_1.txt`**, ..., **`list_for_project_n.txt`:** Txt lists for each project.
- **`project_to_txt.csv`:** Maps projects to their txt list.

#### Detailed File Descriptions

- **Projects:**
Each individual project folder contains the relavent bug reports for that project.

- **Bug Reports:**
Each bug report contains all associated files. The script ignores non-image files.

- **Txt Files:**
Lists each bug report to be processed for a project, with each report specified on a separate line. Unlisted bug reports will be removed.

- **CSV File:**
Format `project_folder_name,txt_file` mapping projects to their respective txt files. Unlisted projects will be ignored.

#### Running the Script

- **Script:** `process_images_with_api.py`
- **Command:**
  ```bash
  python process_images_with_api.py /path/to/directory/for/processing /path/to/directory/with/txts /path/to/csv
  ```
  - `/path/to/directory/for/processing`: Directory where project folders are stored.
  - `/path/to/directory/with/txts`: Directory where txt files are stored.
  - `/path/to/csv`: Path to CSV file specifying which projects to process and their associated txt files.



## Example Result

This section dissects an already executed example of the processing script applied to multiple projects, detailing the file state before and after execution and explaining the changes.

### Example files

- **Before Execution:** Access `example_before.zip` to view the initial state of the files.
- **After Execution:** Access `example_result.zip` to examine the files post-processing.

### Understanding the Execution Process

This example illustrates the script's effects when executed with the following command while in the example directory:
```bash
python ../process_images_with_api.py ./projects ./txts ./projects_to_process.csv
```

### Changes Made During Execution

- **Project Selection:** The `projects_to_process.csv` lists only 2 out of 3 projects present in the directory. Consequently, the third project remains untouched because it was not specified in the CSV.

- **Bug Report Handling:** For each processed project, all bug reports not listed in its corresponding text file were removed.

- **Image Processing:** Each image within the retained bug reports was sent to the OpenAI API for processing. The results are written to two new text files within the relevant bug report folder.

- **Error Handling:** API calls resulting in an error from OpenAI are tracked and retried at the end of the process.


