# b) Shell script to add two numbers passed as command-line arguments

if [ $# -ne 2 ]; then
    echo "Usage :$0 <number1><number2>"
    exit 1
fi

n1="$1"
n2="$2"

sum=$((n1+n2))
echo "Sum of a and b is $sum"