# b) Write a shell script that displays all the links to a file specified as 
#      the first argument to the script. The second argument, which is optional, 
#      can be used to specify in which the search is to begin. If this second argument is not present, 
#      the search is to begin in current working directory. In either case, 
#      the starting directory as well as all its subdirectories at all levels must be searched. 
#      The script need not include any error checking.

target_file="$1"
start_dir="$2"

if [ -z "$start_dir" ]; then
    start_dir="."
fi

inode=$(ls -i "$target_file" | awk '{print $1}')

find "$start_dir" -inum "$inode"