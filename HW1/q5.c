#include <stdio.h> 
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