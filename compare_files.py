import sys
import os

def compare_files(file1_path, file2_path, output_path):
    # Read the contents of file1 and file2
    with open(file1_path, 'r') as file1:
        file1_lines = set(line.strip() for line in file1)

    with open(file2_path, 'r') as file2:
        file2_lines = set(line.strip() for line in file2)

    # Find entries in file1 that are not in file2
    unique_to_file1 = file1_lines - file2_lines

    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        for line in unique_to_file1:
            output_file.write(line + '\n')

    print(f"Entries unique to {file1_path} have been written to {output_path}")

# Example usage:
# compare_files('file1.txt', 'file2.txt', 'output.txt')

def main():
    if len(sys.argv) < 3:
        print("Usage: python unique_lines.py <file1> <file2> [output]")
        sys.exit(1)
    
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_path = sys.argv[3]
    
    compare_files(file1_path, file2_path, output_path)

if __name__ == "__main__":
    main()
