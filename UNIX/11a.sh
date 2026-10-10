# a) Shell script to extract usernames from /etc/passwd using grep.

if [ ! -r /etc/passwd ]; then
    echo "Error: Cannot read /etc/passwd"
    exit 1
fi

echo "Usernames in /etc/passwd:"

# Extract usernames (first field before ':')
cut -d: -f1 /etc/passwd