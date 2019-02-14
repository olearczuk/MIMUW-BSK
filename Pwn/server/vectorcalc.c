#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>
#include <iso646.h>

#define NUM_VARS	26
#define STACK_SIZE	32
#define VECTOR_WIDTH	8

#define TOKEN_START	0
#define TOKEN_VAL	1
#define TOKEN_LP	2
#define TOKEN_ADD	3
#define TOKEN_SUB	4
#define TOKEN_MUL	5
#define TOKEN_DOT	6

struct vector {
	double v[VECTOR_WIDTH];
};

void compute(char *expr, struct vector *vars) {
	struct vector stack_value[STACK_SIZE] = {0};
	int stack_token[STACK_SIZE] = {0};
	int sp = 1;
	stack_token[0] = TOKEN_START;

	int pos = 0;
	int to_var = -1;
	while (isspace(expr[pos]))
		pos++;
	/* Determine if we're assigning to a variable.  */
	if (expr[pos] >= 'a' and expr[pos] <= 'z') {
		int pos_copy = pos + 1;
		while (isspace(expr[pos_copy]))
			pos_copy++;
		if (expr[pos_copy] == '=') {
			to_var = expr[pos] - 'a';
			pos = pos_copy + 1;
		}
	}
	while (1337) {
		while (isspace(expr[pos]))
			pos++;

		/* Perform reductions.  */
		while (true) {
			if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_ADD and stack_token[sp-3] != TOKEN_VAL) {
				/* Unary +.  */
				stack_value[sp-2] = stack_value[sp-1];
				stack_token[sp-2] = TOKEN_VAL;
				sp--;
			} else if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_SUB and stack_token[sp-3] != TOKEN_VAL) {
				/* Unary -.  */
				for (int i = 0; i < VECTOR_WIDTH; i++)
					stack_value[sp-2].v[i] = -stack_value[sp-1].v[i];
				stack_token[sp-2] = TOKEN_VAL;
				sp--;
			} else if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_MUL and stack_token[sp-3] == TOKEN_VAL) {
				/* Multiplication.  */
				for (int i = 0; i < VECTOR_WIDTH; i++)
					stack_value[sp-3].v[i] *= stack_value[sp-1].v[i];
				sp -= 2;
			} else if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_DOT and stack_token[sp-3] == TOKEN_VAL) {
				/* Dot product.  */
				double res = 0;
				for (int i = 0; i < VECTOR_WIDTH; i++)
					res += stack_value[sp-3].v[i] * stack_value[sp-1].v[i];
				for (int i = 0; i < VECTOR_WIDTH; i++)
					stack_value[sp-3].v[i] = res;
				sp -= 2;
			} else if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_ADD and stack_token[sp-3] == TOKEN_VAL and expr[pos] != '*' and expr[pos] != '/') {
				/* Addition.  */
				for (int i = 0; i < VECTOR_WIDTH; i++)
					stack_value[sp-3].v[i] += stack_value[sp-1].v[i];
				sp -= 2;
			} else if (stack_token[sp-1] == TOKEN_VAL and stack_token[sp-2] == TOKEN_SUB and stack_token[sp-3] == TOKEN_VAL and expr[pos] != '*' and expr[pos] != '/') {
				/* Subtraction.  */
				for (int i = 0; i < VECTOR_WIDTH; i++)
					stack_value[sp-3].v[i] -= stack_value[sp-1].v[i];
				sp -= 2;
			} else {
				break;
			}
		}

		if (expr[pos] == '(') {
			/* Left paren -- push on stack, wait for something more interesting.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp++] = TOKEN_LP;
			pos++;
		} else if (expr[pos] == ')') {
			/* Right paren -- verify there's a matching right paren, move the value down the stack.  */
			if (stack_token[sp-2] != TOKEN_LP)
				goto syntax_err;
			stack_token[sp-2] = TOKEN_VAL;
			stack_value[sp-2] = stack_value[sp-1];
			sp--;
			pos++;
		} else if (expr[pos] == '+') {
			/* Addition.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp++] = TOKEN_ADD;
			pos++;
		} else if (expr[pos] == '-') {
			/* Subtraction.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp++] = TOKEN_SUB;
			pos++;
		} else if (expr[pos] == '*') {
			/* Multiplication.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp++] = TOKEN_MUL;
			pos++;
		} else if (expr[pos] == '@') {
			/* Dot product.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp++] = TOKEN_DOT;
			pos++;
		} else if (expr[pos] >= 'a' and expr[pos] <= 'z') {
			/* A variable.  Read it.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp] = TOKEN_VAL;
			stack_value[sp++] = vars[expr[pos] - 'a'];
			pos++;
		} else if (expr[pos] == '{') {
			/* Vector constant.  */
			if (sp > STACK_SIZE)
				goto stack_ovf;
			pos++;
			stack_token[sp] = TOKEN_VAL;
			for (int i = 0; i < VECTOR_WIDTH; i++) {
				char *endptr;
				while (isspace(expr[pos]))
					pos++;
				stack_value[sp].v[i] = strtod(expr + pos, &endptr);
				if (endptr == expr + pos)
					goto val_err;
				pos = endptr - expr;
				while (isspace(expr[pos]))
					pos++;
				if (expr[pos] != (i == VECTOR_WIDTH - 1 ? '}' : ','))
					goto val_err;
				pos++;
			}
			sp++;
		} else if (expr[pos] == 0 or expr[pos] == '\n') {
			/* End of the line.  */
			if (stack_token[sp-2] != TOKEN_START)
				goto syntax_err;
			if (to_var == -1) {
				printf("{");
				for (int i = 0; i < VECTOR_WIDTH; i++) {
					if (i)
						printf(", ");
					printf("%.20e", stack_value[sp-1].v[i]);
				}
				printf("}\n");
			} else {
				vars[to_var] = stack_value[sp-1];
			}
			return;
		} else {
			/* Scalar constant or bust.  */
			char *endptr;
			if (sp > STACK_SIZE)
				goto stack_ovf;
			stack_token[sp] = TOKEN_VAL;
			stack_value[sp].v[0] = strtod(expr + pos, &endptr);
			if (endptr == expr + pos)
				goto val_err;
			pos = endptr - expr;
			for (int i = 1; i < VECTOR_WIDTH; i++)
				stack_value[sp].v[i] = stack_value[sp].v[0];
			sp++;
		}
	}

stack_ovf:
	printf("Stack overflow :(\n");
	exit(1337);
syntax_err:
	printf("Syntax error at position %d :(\n", pos);
	exit(1);
val_err:
	printf("Cannot parse value: %s :(\n", expr + pos);
	exit(1);
}

int main() {
	struct vector vars[26] = {0};
	char buf[1024];
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	while (fgets(buf, sizeof buf, stdin)) {
		compute(buf, vars);
	}
	return 0;
}
