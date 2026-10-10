# b)Shell script to count number of lines, words, and characters in a file.

echo "Enter the file name : "
read file

w=`cat $file|wc -w`
c=`cat $file|wc -c`
l=`cat $file|wc -l`

echo "Number of lines : $l"
echo "Number of words : $w"
echo "Number of characters : $c"