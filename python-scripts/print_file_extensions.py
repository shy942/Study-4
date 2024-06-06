import os
import sys


# gather all extensions from a directory
def get_extensions(base_path):
    unique_extensions = set()
    for root, dirs, files in os.walk(base_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                unique_extensions.add(ext)
    return unique_extensions


def main(base_dir):
    print(get_extensions(base_dir))


# verify 1 command line argument
if __name__ == "__main__":

    if len(sys.argv) == 2:
        base_dir = sys.argv[1]
    else:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)

    main(base_dir)

