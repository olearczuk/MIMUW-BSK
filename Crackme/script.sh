gcc -shared -fPIC decrypt.c -o decrypt.so -ldl
LD_PRELOAD=$PWD/decrypt.so ./bsk01 > pairs_input
python process_pairs.py
rm decrypt.so pairs_input