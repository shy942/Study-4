import os
import zipfile
import shutil
import argparse


# create a destination directory if it does not exist already
def check_directory(path):
    if not os.path.exists(path): 
        response = input(f"The directory {path} does not exist. Create it? (y/n): ")
        if response.lower() == 'y':
            os.makedirs(path)
        else:
            exit()


# loop through zip files in specified directory and extract them to another specified directory
def main(source_dir, destination_dir):
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        exit()

    check_directory(destination_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith('.zip'):
            zip_path = os.path.join(source_dir, filename)
            extraction_path = os.path.join(source_dir, 'extracted')
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_path)
            
            for item in os.listdir(extraction_path):
                item_path = os.path.join(extraction_path, item)
                shutil.move(item_path, destination_dir)
            
            os.remove(zip_path)
            shutil.rmtree(extraction_path)


# directory destinations specified through command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and organize ZIP files")
    parser.add_argument('source_dir', type=str, help='Directory containing ZIP files')
    parser.add_argument('destination_dir', type=str, help='Directory to move extracted folders')
    args = parser.parse_args()

    main(args.source_dir, args.destination_dir)

