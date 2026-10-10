# b) Write a shell script to create a directory, 
#      create a file in it and copy the file to another directory.

echo "Creating source directory 'src'"
mkdir src1

echo "creaing a file 'sample.txt' inside 'src'"
echo "This is sample file">src1/sample.txt

echo "Ceating destination directory"
mkdir dest1

echo "copying 'sample.txt' to 'dest1'"
cp src1/sample.txt dest1

echo "copying operation completed successfully"