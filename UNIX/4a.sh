# a) Write a shell script that accepts two file names as arguments, 
#     checks if the permissions for these files are identical and if the permission are identical, 
#     output common permission and otherwise output each file name followed by its permissions.

if [ $# -ne 2 ]; then
    echo "usage: $0 <file1> <file2>"
    exit 1
fi

file1="$1"
file2="$2"

if [ ! -e "$file1" ]; then
    echo "Error:$file1 does not exist"
    exit 1
fi

if [ ! -e "$file2" ]; then
    echo "Error:$file2 does not exist"
    exit 1
fi

perm1=$(stat -c "%A" "$file1")
perm2=$(stat -c "%A" "$file2")

if [ "$perm1" = "$perm2" ]; then
    echo "Permission are identical : $perm1"
else
    echo "$file1 permission is : $perm1"
    echo "$file2 permission is : $perm2"
fi