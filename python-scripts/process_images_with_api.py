from openai import OpenAI
import base64
import requests
import os
import glob


prompt = "Provide a detailed plain text descriptive paragraph of this image. Then, give an exact plain text monospaced transcript of any and all text in the image."

base_dir = './1'
directories_to_process = 'groundtruthFound_imgui.txt'
image_extensions = ['*.jpg', '*.JPG',  '*.png', '*.PNG']

api_key = 'YOUR_API_KEY'
model = 'gpt-4o'
api_url = 'https://api.openai.com/v1/chat/completions'
max_tokens = 1000



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
    
    if not image_description.strip() or not image_text_transcript.strip():
        print(f"\n\nPotential error. Check txt's at {image_info['dir_path']}. Unformatted output is below.\n")
        print(f"{input_string}\n\n")
    
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
            print(f"Error with sending image to API in {dir_path} upload: {e}")



# find all images to be processed and encode them
def process_and_encode_images(base_directory, image_extensions, directories_to_process):
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
        print(f"Directories not found: {not_found}")

    return encoded_images, dir_count



images_info, dir_count = process_and_encode_images(base_dir, image_extensions, directories_to_process)
print(f"Searched {dir_count} directories and found {len(images_info)} images, send each to OpenAI API?")

user_input = input("(y/n): ")
if user_input.lower() != 'y':
    exit()

send_images_to_api(images_info)


