#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
static void my_ld() {
	typedef void func(uint64_t*, int*);
	uint64_t password;
	// address of decrypt function
	func* f = (func*) 0x4011e0;
	// starting number, we want to process every number 0xfeed + <1 character>
	uint64_t start = 0xfeed00000000;

	for (int i = 0; i < 256; i++) {
		password = start + i;
		printf("%lu ", password);
		f(&password, (int*) 0x4040e0);
		printf("%lu\n", password);
	}
	exit(0);
}
