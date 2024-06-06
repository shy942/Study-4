from openai import OpenAI
import base64
import requests
import os
import glob
import sys
import shutil


image_extensions = ['*.jpg', '*.JPG',  '*.png', '*.PNG']
prompt = "Provide a single detailed plain text descriptive paragraph of this image. Then, give an exact plain text monospaced transcript of any and all text in the image."

api_key = 'YOUR_API_KEY'
model = 'gpt-4o'
api_url = 'https://api.openai.com/v1/chat/completions'
max_tokens = 2500



# format the GPT's output into .txt files, stripping away unecessary formatting and headers
def write_to_files(image_info, input_string):
    image_description = ''
    image_text_transcript = ''
    in_code_block = False
    ignore_rest = False
    i = 0
    
    while i < len(input_string):
        if (input_string[i:i+2] == '##' or input_string[i:i+2] == '**') and not in_code_block:
            i += 2

            while i < len(input_string) and input_string[i] != '\n':
                i += 1
            
            if i < len(input_string) and input_string[i] == '\n':
                i += 1
            continue

        if input_string[i:i+3] == '```':
            in_code_block = not in_code_block
            ignore_rest = False
            if not in_code_block:
                break
            i += 3
            continue
        
        if not in_code_block:
            if i + 1 < len(input_string) and input_string[i] == '\n' and input_string[i + 1] == '\n':
                ignore_rest = True
                i += 2
                continue
            elif input_string[i] == '\n':
                image_description += ' '
                i += 1
                continue

        if ignore_rest:
            i += 1
            continue
        
        if in_code_block:
            image_text_transcript += input_string[i]
        else:
            image_description += input_string[i]
        i += 1
    
    
    description_path = os.path.join(image_info['dir_path'], f"{image_info['file_name']}ImageDescription.txt")
    content_path = os.path.join(image_info['dir_path'], f"{image_info['file_name']}ImageContent.txt")
    
    with open(description_path, 'w') as file:
        file.write(image_description)
    with open(content_path, 'w') as file:
        file.write('\n'.join(image_text_transcript.split('\n')[1:]))



# send each image to the openai API and write its response to .txt files
def send_images_to_api(images_info):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
           }
    
    for image_info in images_info:
        dir_path = image_info['dir_path']
        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        { 
                            'type': 'image_url', 
                            'image_url': { 
                                'url': f"data:image/{image_info['extension']};base64,{image_info['encoded']}"
                            } 
                        }
                    ]
                }
            ],
            'max_tokens': max_tokens
        }
        try:
            
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            write_to_files(image_info, str(data['choices'][0]['message']['content']))
            print(f"Wrote .txt's in {dir_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending {image_info['file_name']} image to API located in {dir_path}: \n{e}")
            errored_requests.append(image_info)
            



# find all images to be processed for a project and encode them
def process_and_encode_images(base_directory, directories_to_process):
    encoded_images = []
    dir_count = 0

    with open(directories_to_process, 'r') as file:
        allowed_dirs = {line.strip() for line in file.readlines()}

    found_dirs = set()
    
    for root, dirs, files in os.walk(base_directory):
        relative_dir_path = os.path.relpath(root, base_directory)
        
        if relative_dir_path in allowed_dirs:
            found_dirs.add(relative_dir_path)
            dir_count += 1

            for extension in image_extensions:
                for image_path in glob.glob(os.path.join(root, extension)):
                    file_name = os.path.splitext(os.path.basename(image_path))[0]
                    with open(image_path, 'rb') as file:
                        encoded_string = base64.b64encode(file.read()).decode('utf-8')
                        image_info = {
                            'dir_path': root,
                            'file_name': file_name,
                            'extension': extension[2:],
                            'encoded': encoded_string,
                        }
                        encoded_images.append(image_info)
    
    not_found = allowed_dirs - found_dirs
    
    if not_found:
        print(f"Creating missing bug report txt for the following directories not found: {not_found}")
        
        file_path = f"{base_directory}/missing_bug_reports.txt"
        with open(file_path, "w") as file:
            file.write("Following bug reports are not found:\n")
            for item in not_found:
                 file.write(f"{item}\n")

    return encoded_images, dir_count



# remove all directories from a specified path except the ones listed in a txt
def keep_only_listed_directories(base_directory, list_file):
    with open(list_file, 'r') as file:
        keep_dirs = {line.strip() for line in file}

    all_dirs = {name for name in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, name))}

    dirs_to_delete = all_dirs - keep_dirs

    for dir_name in dirs_to_delete:
        dir_path = os.path.join(base_directory, dir_name)
        shutil.rmtree(dir_path)

    return len(dirs_to_delete)



# each line of 2 items in a csv becomes a dictionary, a list of all dictionaries are returned
def parse_csv(file_path):
    all_projects = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split(',')

                if len(parts) == 2:
                    project_dict = {'project': parts[0], 'identifier': parts[1]}
                    all_projects.append(project_dict)
                else:
                    raise ValueError("Each line must contain exactly two items separated by a comma.")
    
    except Exception as e:
        print(f"Failed to read or parse the file: {e}")
        exit(1)
    
    return all_projects



# loop through each project specified in the csv, sending the specified images to the api
errored_requests = []
def main(projects_dir, txts_dir, csv_path):
    
    all_projects = parse_csv(csv_path)
    
    for project in all_projects:
        project_path = os.path.join(projects_dir, project['project'])
        
        match_count = 0
        txt_file_path = None
        for txt_file in os.listdir(txts_dir):
            if project['identifier'] in txt_file:
                match_count += 1
                txt_file_path = os.path.join(txts_dir, txt_file)

        if txt_file_path and match_count == 1:

            number_removed = keep_only_listed_directories(project_path, txt_file_path)
            print(f"Removed {number_removed} unecessary directories from project {project['project']}")

            images_info, dir_count = process_and_encode_images(project_path, txt_file_path)
            print(f"Searched {dir_count} directories in project {project['project']} using identifier {project['identifier']}")
            print(f"Found {len(images_info)} images - sending each to OpenAI API")
            send_images_to_api(images_info)

        elif not txt_file_path:
            print(f"No matching txt file found for identifier {project['identifier']} in {txts_dir}")
        else:
            print(f"txt identifier {project['identifier']} not unique enough: {match_count} files detected")


    while len(errored_requests) > 0:
        print(f"There were {len(errored_requests)} errored requests. Do you want to try sending them again? (y/n)")
        user_input = input().strip().lower()
        
        if user_input == 'y':

            images_info = errored_requests.copy()
            errored_requests.clear()
            send_images_to_api(images_info)

        else:
            break



# verify 3 command line arguments
if __name__ == "__main__":
    
    if len(sys.argv) == 4:
        projects_dir = sys.argv[1]
        txts_dir = sys.argv[2]
        csv_path = sys.argv[3]
    
    else:
        print("Usage: python process_images_with_api.py <images_dir> <txts_dir> <csv_path>")
        sys.exit(1)
    
    main(projects_dir, txts_dir, csv_path)



