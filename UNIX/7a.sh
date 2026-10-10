# a) Shell script to print the multiplication table of a given number.

echo "Enter the number : "
read n

echo "The multiplication num is :"
for i in $(seq 1 10)
do
    res=$((n*i))
    echo "$n x $i = $res"
done