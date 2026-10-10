# b) Shell script to find factorial of a number using a while loop.

echo "Enter the number :"
read num

fact=1
i=1

while [ $i -le $num ]
do
    fact=$((fact * i))
    i=$((i+1))
done

echo "The factorial of the number is : $fact"