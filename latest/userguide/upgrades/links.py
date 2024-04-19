import os
import re
import sys

# Function to convert markdown anchor links to asciidoc anchor links
def convert_anchor_links(text):
    markdown_anchor_pattern = r'\[([^\]]+)\]\(#([^)]+)\)'
    asciidoc_anchor_pattern = r'xref:\2[\1]'
    return re.sub(markdown_anchor_pattern, asciidoc_anchor_pattern, text)

# Function to convert markdown URL links to asciidoc URL links
def convert_url_links(text):
    markdown_url_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    asciidoc_url_pattern = r'\2[\1]'
    return re.sub(markdown_url_pattern, asciidoc_url_pattern, text)

# Function to process a single file
def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        updated_content = convert_anchor_links(content)
        updated_content = convert_url_links(updated_content)
    with open(file_path, 'w') as file:
        file.write(updated_content)
    print(f"Processed file: {file_path}")

# Function to process all files in a directory
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

# Main function
def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_file(file_path)
        else:
            print(f"File not found: {file_path}")
    else:
        directory_path = './'  # Current directory
        process_directory(directory_path)

if __name__ == '__main__':
    main()