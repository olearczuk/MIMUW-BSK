# Overiew
We were given files secureproc.py and securedemo.py (code was running on a server). Our goal was to get content of files flag_easy.txt (easier task) and flag_hard.txt (harder task). Difference between both task was limited amount of allowed requests in harder version.

# Analysis of program
## Secureproc
- read_byte allows to read current bytes of data, reading key is obviously impossible
- write_byte allows to overwrite bytes of both data and key. Additionaly, overwriting last byte of data results in changing data to AES(key, data)

## Securedemo
- produces random key
- encodes FLAG_EASY/FLAG_HARD (depends on scenario client chooses) using CBC algorithm and sends ciphertext (including initialization vector)
- it is possible for client to call read_byte and write_byte functions by sending specific communication

# Both variants of solutions

## Solution of easier scenario
- firstly I check what is outcome of AES(key, 0)
- then I brute force consecutive bytes of key
  - for each possible value of byte key (0x00 - 0xff) I check outcome of AES(modified_key, data)
  - if it is equal to previosly checked value, then I found value of current byte
- this way I have value of key so I can decrypt sent ciphertext

## Solution of harder scenario
### Collecting needed information
- I get outcome of AES(key', 0) for key'
  - <1st byte of key> rest 0x00
  - <1st byte of key> <2nd byte of key> rest 0x00
  - ...
  - <1st byte of key> ... <15th byte of key> rest 0x00
  - whole original key
- I get that by going backwards and changing bytes of key to 0x00 and setting whole data to 0x00.

### Getting key
- using collected information I can (locally!) get content of key by
  - I check for which 1st byte key <1st byte> rest 0x00 produces the same outcome as stored
  - I check for which 2nd byte key <1st byte> <2nd byte> rest 0x00 produces the same outcome as stored
  - ...
  - I check for which 16th byte key <1st byte> ... <16th byte> produces the same outcome as stored
- Having key I can decrypt ciphertext 

## Differences between solutions
- in easier variant all the processing occured on the server side
- in harder variant there was little processing on server side (only getting needed information), brute forcing key's bytes happened on client side

# Usage
## Server
Go to server folder, install requirements and 
```sh
python3 securedemo.py
``` 
## Client
Instal requirements and 
```sh
python3 easy.py # easy scenario
python3 hard.py # hard scenario
```
