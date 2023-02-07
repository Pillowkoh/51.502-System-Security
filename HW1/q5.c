#include <stdio.h> 
#include <stdlib.h>

int main(int argc, char *argv[]){ 
    int arg1, arg2;
 
    if (argc != 3)
        return -1; 
 
    arg1 = atoi(argv[1]); 
    arg2 = atoi(argv[2]); 
    if (arg1 < 0 || arg2 < 0) 
        return -1; 
    
    if (arg1 + arg2 >= 0) 
        return -1; 
    printf("ACCESS GRANTED\n"); 
}

/* 
### ANSWER ###

argv and argc are how command line arguments are passed to main() in C and C++.
argc will be the number of strings pointed to by argv. This will (in practice) be 1 plus the number of arguments, as virtually all implementations will prepend the name of the program to the array.

atoi will cast the string parsed in the argument to an integer.

Given that arg1 and arg2 are initialised as signed integers, we can exploit the integer overflow vulnerability to bypass all if block conditions.

By parsing 2147483647 and 1 as arguments to the main function, we would be able to get the application to print "ACCESS GRANTED".

### EXPLANATION ###
As arg1 and arg2 are initialised as signed integers, 4 bytes are assigned to each of this variables.

2147483647  is represented as 0b 0111 1111 1111 1111 1111 1111 1111 1111
1           is represented as 0b 0000 0000 0000 0000 0000 0000 0000 0001

When added together, their sum in binary is represented as 0b 1000 0000 0000 0000 0000 0000 0000 0000 which is equivalent to -2147483648 in decimal as the most significant bit on the left is set to 1.

Therefore, we will be able to get the "ACCESS GRANTED" message.

### HOW TO RUN CODE ###
1. To compile c code, run the following command in the terminal:
    'gcc q5.c -o q5'
2. Run compiled c code in the terminal with:
    './q5 2147483647 1'         
*/


