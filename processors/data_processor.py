import os

# Function to split the given content into smaller chunks (by paragraphs)
def split_text(content):
    return content.split("\n\n")

# Function to process all text files in 'data/raw_text/' and save the processed text in the 'data/processed/
def process_all():
    input_dir = "data/raw_text/"
    output_dir = "data/processed/"
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterating over all files in the input directory
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = split_text(content)
            
            output_file_path = os.path.join(output_dir, file_name)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(chunks))
            print(f"Processed and saved: {output_file_path}")

if __name__ == "__main__":
    process_all()
    print("All files processed and saved in 'data/processed/'.")
