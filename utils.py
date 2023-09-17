# Function to read system content from a file
def read_prompt_file(filename):
    with open(f'./prompts/{filename}', 'r') as file:
        return file.read()