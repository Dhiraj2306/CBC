# b) Shell script for a menu-driven program to list files, view current directory, and exit.

while true
do
echo "1. List files"
echo "2. View current working directory"
echo "3. Exit"
echo "Enter your choice [1-3] : "
read choice

case $choice in
1)
    echo "list of files in cwd : "
    ls -l
    ;;
2) 
    echo "Current working directory : "
    pwd
    ;;
3)
    echo "Exiting"
    exit 0
    ;;
*)
    echo "Invalid choice. Please enter 1, 2, or 3"
    ;;
esac
done