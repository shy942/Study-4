import os

base_dir = './1'


def get_extensions(base_path):
    unique_extensions = set()
    for root, dirs, files in os.walk(base_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                unique_extensions.add(ext)
    return unique_extensions


print(get_extensions(base_dir))


