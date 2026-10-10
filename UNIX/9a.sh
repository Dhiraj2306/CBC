# a) Shell script to check whether a string is a palindrome.

echo "Enter a string : "
read str

rev_str=$( echo "$str" |rev)

if [ "$str" = "$rev_str" ]; then
    echo "string is palindrome"
else 
    echo "string is not palindrome"
fi