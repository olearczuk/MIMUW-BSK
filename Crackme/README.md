# Overview
Idea of this task was to find flag - password, that will be accepted by the program. I was using peda extension for gdb.

# Analysis of program
## Main 
You are asked to write password. First thing that is checked is length of password. IF it is not equal to 29, program writes 'Wrong.' and exits.
Then in a loop program uses local function decrypt to decrypt some of inner code.
Actually it decodes function check. Set of commands
```sh
gdb bsk01
pd check
```
and 
```sh
gdb bsk01
b check
r
# write anything that is 29 characters long -> aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
pd check
```
produce totally different output.
Next function check is called. It returns 0, when password is accepted, and 1, when rejected.
## Decrypt
Function decrypt takes 2 arguments: pointer and table.
The only important thing about that function is fact, that it overwrites first argument with new value.
## Check
Program loops over characters of given password and calls function decrypt with 2 arguments. Pointer to word 0xfeed000000<hex code of current character>, and local table (0x4040e0 address).
Result of decrypt is then compared with value in proper index of table correct_pass (0x404060 address). This loop has 29 rounds (for every char in given password, and every index of correct_pass table). Check accepts password, if every 29 comparisons were positive.

# Description of solution
## script.sh
This file wraps all commands needed to extract flag. Write sh script.sh to reveal hidden flag.
## decrypt.c file
This code basically writes out pairs (word, result), when word is 0xfeed000000<hex represenation of numbers 0 to 255> and result is result of function decrypt with arguments pointer to word, and address to table 0x4040e0. Thanks to preload it has access to inner access and thanks to __attribute__((constructor)) it is executed before the original program starts. Output is redirected to file pairs_input
## process_pairs.py
This program contains values stored in table correct_pass (0x404060 address). I got this values by running command
```sh
x/29wx correct_pass
```
and then just copied it to local array. Finally using data generated using decrypt.c file we can reveal the flag. For every element in array correct_pass we find argument, for which decrypt's result was equal to current element.
Then we can extract hex code of character from argument, and actual character.
Flag is sum of all produced characters


