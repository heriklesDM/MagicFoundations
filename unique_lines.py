
import sys
import os

def get_unique_lines(folder_path, output_file="unique_lines_output.txt"):
    """
    Process each text file in the specified folder, ignoring lines that start with numbers,
    and saves each unique line to a single output file.

    Parameters:
    - folder_path (str): Path to the folder containing text files to process.
    - output_file (str): Path for the output file with unique lines. Defaults to "unique_lines_output.txt".
    """
    
    unique_lines = set()
    
    # Check if the specified folder exists
    if not os.path.isdir(folder_path):
        print("The specified folder does not exist.")
        return
    
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Only process text files
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Strip leading/trailing whitespace and check if line starts with a number
                    stripped_line = line.strip()
                    if not stripped_line or stripped_line[0].isdigit():
                        continue
                    
                    # Add line to the set of unique lines
                    unique_lines.add(stripped_line)
    
    # Write all unique lines to the output file
    with open(output_file, 'w', encoding='utf-8') as output:
        for line in sorted(unique_lines):  # Optional: Sort lines alphabetically before saving
            output.write(line + '\n')
    
    print(f"Unique lines have been saved to {output_file}")

# Example usage:
# get_unique_lines("path/to/your/folder")
def main():
    if len(sys.argv) < 2:
        print("Usage: python unique_lines.py <folder_path> [output_file]")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "unique_lines_output.txt"
    
    get_unique_lines(folder_path, output_file)

if __name__ == "__main__":
    main()
