import os
import re

# Function to convert markdown links to asciidoc links
def convert_links(text):
    markdown_link_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    asciidoc_link_pattern = r'\2[\1]'
    return re.sub(markdown_link_pattern, asciidoc_link_pattern, text)

# Function to process a single file
def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    updated_content = convert_links(content)

    with open(file_path, 'w') as file:
        file.write(updated_content)

# Function to process all .adoc files in a directory
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.adoc'):
                file_path = os.path.join(root, file)
                process_file(file_path)

# Example usage
directory_path = './'  # Current directory
process_directory(directory_path)