# b) Shell script to count the number of files and directories in a given path.

#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <directory>"
  exit 1
fi

path="$1"

if [ ! -d "$path" ]; then
  echo "Not a valid directory: $path"
  exit 1
fi

file_count=$(find "$path" -type f | wc -l)
dir_count=$(find "$path" -type d | wc -l)

echo "In the directory: $path"
echo "Number of files: $file_count"
echo "Number of directories: $dir_count"