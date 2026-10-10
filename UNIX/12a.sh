# a) Write a shell script that accept one or more filenames as argument and 
#      convert all of them to uppercase, 
#      provided they exist in current directory.

# Check if at least one filename is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <file1> [file2] ..."
    exit 1
fi

# Loop through all arguments
for file in "$@"; do
    if [ -f "$file" ]; then
        upper_file="UPPER_$file"
        tr '[:lower:]' '[:upper:]' < "$file" > "$upper_file"
        echo "Converted '$file' to uppercase and saved as '$upper_file'"
    else
        echo "File '$file' does not exist in current directory."
    fi
done