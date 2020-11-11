gcc -fPIC -c $1.S -o $1.o
gcc -fPIC $1.o -o $1
./$1