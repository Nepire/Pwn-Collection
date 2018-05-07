#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
 
void print_menu();
void add_paper();
void delete_paper();
void secret();
int get_num();
void get_input(char *buffer, int size, int no_should_fill_full);
void gg();
 
char *link_list[10];
 
int main()
{
    setbuf(stdout, 0);
    int choice;
    get_name();
    while (1)
    {
        print_menu();
        choice = get_num();
        switch (choice)
        {
            case 1:
                add_paper();
                break;
            case 2:
                delete_paper();
                break;
            case 3:
                secret();
                break;
        }
    }
}
void gg()
{
    system('/bin/sh')
    return ;
}
void secret()
{
    int result;
    char luck_number;
    unsigned int choice;
    printf("enter your luck number:");
    scanf("%ld",&luck_number)
    puts("Maybe you want continue manage paper?")
    while(1)
    {
        while (1)
        {
            print_menu();
            choice = get_num();
            result = choice;
            if(choice != 1)
            {
                break;
            }
            add_paper();
        }
        if(choice != 2)
        {
            break;
        }
        delete_paper();
    }
    return result;
}
void delete_paper()
{
    int index;
    printf("which paper you want to delete,please enter it's index(0-9):");
    scanf("%d", &index);
    if (index < 0 || index > 9)
        exit(1);
    free(link_list[index]);
    puts("delete success !");
}
void add_paper()
{
    int index;
    int length;
    printf("Input the index you want to store(0-9):");
    scanf("%d", &index);
    if (index < 0 || index > 9)
        exit(1);
    printf("How long you will enter:");
    scanf("%d", &length);
    if (length < 0 || length > 1024)
        exit(1);
    link_list[index] = malloc(length);
    if (link_list[index] == NULL)
        exit(1);
    printf("please enter your content:");
    get_input(link_list[index]);
    printf("add success!\n");
}
void print_menu()
{
    puts("Welcome to use the paper management system!");
    puts("1 add paper");
    puts("2 delete paper");
}
void get_input(char *buffer, int size, int no_should_fill_full)
{
    int index = 0;
    char *current_location;
    int current_input_size;
    while (1)
    {
        current_location = buffer+index;
        current_input_size = fread(buffer+index, 1, 1, stdin);
        if (current_input_size <= 0)
        {
            break;
        }
        if (*current_location == '\n' && no_should_fill_full)
        {
            if (index)
            {
                *current_location = 0;
                return;
            }       
        }
        else
        {
            index++;
            if (index >= size)
                break;
        }
    }
}
int get_num()
{
    int result;
    char input[48];
    char *end_ptr;
     
    get_input(input, 48, 1);
    result = strtol(input, &end_ptr, 0);
    if (input == end_ptr)
    {
        printf("%s input is not start with number!\n", input);
        result = get_num();
    }
    return result;
}