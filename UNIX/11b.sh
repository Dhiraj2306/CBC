# b) Shell script to remove duplicate lines from a file using sort and uniq.

# Prompt the user for the file name
echo "Enter the file name: "
read filename

# Check if file exists
if [ ! -f "$filename" ]; then
    echo "Error: File '$filename' does not exist."
    exit 1
fi

# Output file name
output="unique_$filename"

# Sort and remove duplicates
sort "$filename" | uniq > "$output"

echo "Duplicate lines removed. Output saved to '$output'."