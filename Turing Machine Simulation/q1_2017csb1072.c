#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define MAXLEN 4096
#define SYMBOLS 8
#define MAXINPUT 20

int num_states = 0;
int step_counter = 0;
char tape_symbols[] = {'0', '1', '#', '$', ' ', 'A', 'B'};
typedef struct state state;
typedef struct state_transition {
	state* cur;
	char symbol_read;
	state* to;
	char symbol_replaced;
	char movement;
} state_transition;

struct state {
 	int state_id;
	int num_transition;
	state_transition list_transition[SYMBOLS];
};

void create_state(state* new_state) {
	new_state->state_id = ++num_states;
	new_state->num_transition = 0;
}

void add_state_transition(state* cur, state* to, char symbol_read, char symbol_replaced, char movement) {
	state_transition* new_transition = &cur->list_transition[cur->num_transition++];
	new_transition->cur = cur;
	new_transition->to = to;
	new_transition->symbol_read = symbol_read, new_transition->symbol_replaced = symbol_replaced, new_transition->movement = movement;
}
void print_tape(char* output);
state* perform_state_transition(state* cur, char symbol_read, char** tape_head) {
	for (int i = 0; i < cur->num_transition; ++i) {
		if (cur->list_transition[i].symbol_read == symbol_read) {
			**tape_head = cur->list_transition[i].symbol_replaced;
			if (cur->list_transition[i].movement == 'L') --(*tape_head);
			else ++(*tape_head);
			printf("%d: %c %c %c\n", step_counter++, symbol_read, cur->list_transition[i].symbol_replaced, cur->list_transition[i].movement);
			return cur->list_transition[i].to;
		}
	}
	assert(1 == 0);
}

typedef struct TM {
	char* tape_head;
	char tape[MAXLEN];
} TM;

void initalize_TM(char input[], TM* tm) {
	for (int i = 0; i<MAXLEN; ++i) tm->tape[i] = ' ';
	char* begin_input = tm->tape + 1;
	for (int i = 0; input[i] != '\0'; ++i) begin_input[i] = input[i];
	tm->tape_head = begin_input;
}

void print_tape(char* output) {
	if (*output == ' ') *output = '0';
	while (*output != ' ') {
		printf("%c", *output);
		++output;
	}
	printf("\n");
}

void add_terminate_sym(TM* tm, char symbol) {
	int nstate = 2;
	state states[nstate];
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	state* cur_state = states;
	for (int i = 0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states, states + 1, ' ', symbol, 'L');
			add_state_transition(states + 1, NULL, ' ', ' ', 'R');
		} else {
			add_state_transition(states, states, tape_symbols[i], tape_symbols[i], 'R');
			add_state_transition(states + 1, states + 1, tape_symbols[i], tape_symbols[i], 'L');
		}
	}
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
} 

void pad_inputs(TM* tm, char sym1, char sym2) {
	int nstate = 32;
	state states[nstate];
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	add_state_transition(states, states, '0', '0', 'R');
	add_state_transition(states, states, '1', '1', 'R');
	add_state_transition(states, states, sym1, sym1, 'R');
	add_state_transition(states, states + 1, sym2, sym2, 'R');
	for (int i = 0; i < 20; ++i) {
		add_state_transition(states + 1 + i, states + 2 + i, ' ', '0', 'R');
	}
	add_state_transition(states + 21, states + 22, ' ', ' ', 'L');
	add_state_transition(states + 22, states + 22, '0', '0', 'L');
	add_state_transition(states + 22, states + 22, '1', '1', 'L');
	add_state_transition(states + 22, states + 22, sym2, sym2, 'L');
	add_state_transition(states + 22, states + 23, sym1, sym1, 'L');
	add_state_transition(states + 23, states + 23, 'A', 'A', 'L');
	add_state_transition(states + 23, states + 23, 'B', 'B', 'L');
	add_state_transition(states + 23, states + 24, '0', 'A', 'R');
	add_state_transition(states + 24, states + 24, 'A', 'A', 'R');
	add_state_transition(states + 24, states + 24, 'B', 'B', 'R');
	add_state_transition(states + 24, states + 24, '0', '0', 'R');
	add_state_transition(states + 24, states + 24, '1', '1', 'R');
	add_state_transition(states + 24, states + 24, sym2, sym2, 'R');
	add_state_transition(states + 24, states + 24, sym1, sym1, 'R');
	add_state_transition(states + 24, states + 25, ' ', ' ', 'L');
	add_state_transition(states + 25, states + 25, 'A', 'A', 'L');
	add_state_transition(states + 25, states + 25, 'B', 'B', 'L');
	add_state_transition(states + 25, states + 22, '0', 'A', 'L');

	add_state_transition(states + 23, states + 26, '1', 'B', 'R');
	add_state_transition(states + 26, states + 26, 'A', 'A', 'R');
	add_state_transition(states + 26, states + 26, 'B', 'B', 'R');
	add_state_transition(states + 26, states + 26, '0', '0', 'R');
	add_state_transition(states + 26, states + 26, '1', '1', 'R');
	add_state_transition(states + 26, states + 26, sym2, sym2, 'R');
	add_state_transition(states + 26, states + 26, sym1, sym1, 'R');
	add_state_transition(states + 26, states + 27, ' ', ' ', 'L');
	add_state_transition(states + 27, states + 27, 'A', 'A', 'L');
	add_state_transition(states + 27, states + 27, 'B', 'B', 'L');
	add_state_transition(states + 27, states + 22, '0', 'B', 'L');
	add_state_transition(states + 23, states + 28, ' ', ' ', 'R');
	add_state_transition(states + 28, states + 28, 'A', ' ', 'R');
	add_state_transition(states + 28, states + 28, 'B', ' ', 'R');
	add_state_transition(states + 28, states + 29, sym1, ' ', 'R');

	add_state_transition(states + 29, states + 29, '0', '0', 'R');
	add_state_transition(states + 29, states + 29, '1', '1', 'R');
	add_state_transition(states + 29, states + 30, sym2, sym2, 'R');
	add_state_transition(states + 30, states + 30, '0', '0', 'R');
	add_state_transition(states + 30, states + 30, 'A', '0', 'R');
	add_state_transition(states + 30, states + 30, 'B', '1', 'R');
	add_state_transition(states + 30, states + 31, ' ', ' ', 'L');
	add_state_transition(states + 31, states + 31, '0', '0', 'L');
	add_state_transition(states + 31, states + 31, '1', '1', 'L');
	add_state_transition(states + 31, states + 31, sym2, sym2, 'L');
	add_state_transition(states + 31, NULL, ' ', ' ', 'R');
	state* cur_state = states;
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
} 

void find_remainder(TM* tm) {
	int nstate = 42;
	state states[nstate];
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	state* cur_state = states;
	add_state_transition(states, states, '0', '0', 'R');
	add_state_transition(states, states, '1', '1', 'R');
	add_state_transition(states, states + 1, '#', '#', 'L');

	add_state_transition(states + 1, states + 2, '0', 'A', 'R');
	add_state_transition(states + 2, states + 2, '#', '#', 'R');
	add_state_transition(states + 2, states + 2, 'A', 'A', 'R');
	add_state_transition(states + 2, states + 2, 'B', 'B', 'R');
	add_state_transition(states + 2, states + 2, '0', '0', 'R');
	add_state_transition(states + 2, states + 2, '1', '1', 'R');
	add_state_transition(states + 2, states + 3, '$', '$', 'L');
	add_state_transition(states + 3, states + 3, 'A', 'A', 'L');
	add_state_transition(states + 3, states + 3, 'B', 'B', 'L');

	add_state_transition(states + 3, states + 4, '0', 'A', 'R');
	add_state_transition(states + 3, states + 4, '#', '#', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 4, states + 5, ' ', '0', 'L');
		} else {
			add_state_transition(states + 4, states + 4, tape_symbols[i], tape_symbols[i], 'R');
			if (tape_symbols[i] == '#') add_state_transition(states + 5, states + 6, '#', '#', 'L');
			add_state_transition(states + 5, states + 5, tape_symbols[i], tape_symbols[i], 'L');
		}
	}
	add_state_transition(states + 6, states + 6, 'A', 'A', 'L');
	add_state_transition(states + 6, states + 6, 'B', 'B', 'L');
	add_state_transition(states + 6, states + 7, '1', '1', 'R');
	add_state_transition(states + 6, states + 7, '0', '0', 'R');
	add_state_transition(states + 6, states + 31, ' ', ' ', 'R');
	add_state_transition(states + 7, states + 1, 'A', 'A', 'L');
	add_state_transition(states + 7, states + 1, 'B', 'B', 'L');

	add_state_transition(states + 3, states + 8, '1', 'B', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 8, states + 9, ' ', '1', 'L');
		} else {
			add_state_transition(states + 8, states + 8, tape_symbols[i], tape_symbols[i], 'R');
			if (tape_symbols[i] == '#') add_state_transition(states + 9, states + 10, '#', '#', 'L');
			add_state_transition(states + 9, states + 9, tape_symbols[i], tape_symbols[i], 'L');
		}
	}
	add_state_transition(states + 10, states + 10, 'A', 'A', 'L');
	add_state_transition(states + 10, states + 10, 'B', 'B', 'L');
	add_state_transition(states + 10, states + 11, '1', '1', 'R');
	add_state_transition(states + 10, states + 11, '0', '0', 'R');
	add_state_transition(states + 10, states + 31, ' ', ' ', 'R');
	add_state_transition(states + 11, states + 16, 'A', 'A', 'L');
	add_state_transition(states + 11, states + 16, 'B', 'B', 'L');

	add_state_transition(states + 1, states + 12, '1', 'B', 'R');
	add_state_transition(states + 12, states + 12, '#', '#', 'R');
	add_state_transition(states + 12, states + 12, 'A', 'A', 'R');
	add_state_transition(states + 12, states + 12, 'B', 'B', 'R');
	add_state_transition(states + 12, states + 12, '0', '0', 'R');
	add_state_transition(states + 12, states + 12, '1', '1', 'R');
	add_state_transition(states + 12, states + 13, '$', '$', 'L');
	add_state_transition(states + 13, states + 13, 'A', 'A', 'L');
	add_state_transition(states + 13, states + 13, 'B', 'B', 'L');

	add_state_transition(states + 13, states + 14, '0', 'A', 'R');
	add_state_transition(states + 13, states + 14, '#', '#', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 14, states + 5, ' ', '1', 'L');
		} else {
			add_state_transition(states + 14, states + 14, tape_symbols[i], tape_symbols[i], 'R');
		}
	}
	add_state_transition(states + 13, states + 15, '1', 'B', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 15, states + 5, ' ', '0', 'L');
		} else {
			add_state_transition(states + 15, states + 15, tape_symbols[i], tape_symbols[i], 'R');
		}
	}

	add_state_transition(states + 16, states + 17, '0', 'A', 'R');
	add_state_transition(states + 17, states + 17, '#', '#', 'R');
	add_state_transition(states + 17, states + 17, 'A', 'A', 'R');
	add_state_transition(states + 17, states + 17, 'B', 'B', 'R');
	add_state_transition(states + 17, states + 17, '0', '0', 'R');
	add_state_transition(states + 17, states + 17, '1', '1', 'R');
	add_state_transition(states + 17, states + 18, '$', '$', 'L');
	add_state_transition(states + 18, states + 18, 'A', 'A', 'L');
	add_state_transition(states + 18, states + 18, 'B', 'B', 'L');

	add_state_transition(states + 18, states + 19, '0', 'A', 'R');
	add_state_transition(states + 18, states + 19, '#', '#', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 19, states + 9, ' ', '1', 'L');
		} else {
			add_state_transition(states + 19, states + 19, tape_symbols[i], tape_symbols[i], 'R');
		}
	}
	add_state_transition(states + 18, states + 20, '1', 'B', 'R'); //replaced state 23 with 20.
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 20, states + 9, ' ', '0', 'L');
		} else {
			add_state_transition(states + 20, states + 20, tape_symbols[i], tape_symbols[i], 'R');
		}
	}
	add_state_transition(states + 16, states + 27, '1', 'B', 'R');
	add_state_transition(states + 27, states + 27, '#', '#', 'R');
	add_state_transition(states + 27, states + 27, 'A', 'A', 'R');
	add_state_transition(states + 27, states + 27, 'B', 'B', 'R');
	add_state_transition(states + 27, states + 27, '0', '0', 'R');
	add_state_transition(states + 27, states + 27, '1', '1', 'R');
	add_state_transition(states + 27, states + 28, '$', '$', 'L');
	add_state_transition(states + 28, states + 28, 'A', 'A', 'L');
	add_state_transition(states + 28, states + 28, 'B', 'B', 'L');

	add_state_transition(states + 28, states + 29, '0', 'A', 'R');
	add_state_transition(states + 28, states + 29, '#', '#', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 29, states + 5, ' ', '0', 'L');
		} else {
			add_state_transition(states + 29, states + 29, tape_symbols[i], tape_symbols[i], 'R');
		}
	}
	add_state_transition(states + 28, states + 30, '1', 'B', 'R');
	for (int i =0; i < SYMBOLS; ++i) {
		if (tape_symbols[i] == ' ') {
			add_state_transition(states + 30, states + 9, ' ', '1', 'L');
		} else {
			add_state_transition(states + 30, states + 30, tape_symbols[i], tape_symbols[i], 'R');
		}
	}
	add_state_transition(states + 31, states + 31, 'A', 'A', 'R');
	add_state_transition(states + 31, states + 31, 'B', 'B', 'R');
	add_state_transition(states + 31, states + 31, '#', '#', 'R');
	add_state_transition(states + 31, states + 21, '$', '$', 'R');
	add_state_transition(states + 21, states + 21, '0', '0', 'R');
	add_state_transition(states + 21, states + 21, '1', '1', 'R');
	add_state_transition(states + 21, states + 22, ' ', ' ', 'L');
	add_state_transition(states + 22, states + 39, '1', ' ', 'L'); //go to reset A.
	add_state_transition(states + 22, states + 23, '0', '0', 'R');
	add_state_transition(states + 23, states + 24, ' ', ' ', 'L');
	
	add_state_transition(states + 24, states + 25, '0', ' ', 'L');
	add_state_transition(states + 25, states + 25, '0', '0', 'L');
	add_state_transition(states + 25, states + 25, '1', '1', 'L');
	add_state_transition(states + 25, states + 25, 'A', '0', 'L');
	add_state_transition(states + 25, states + 25, 'B', '1', 'L');
	add_state_transition(states + 25, states + 26, '#', '#', 'L');
	add_state_transition(states + 25, states + 25, '$', '$', 'L');
	add_state_transition(states + 26, states + 26, 'A', 'A', 'L');
	add_state_transition(states + 26, states + 26, 'B', 'B', 'L');
	add_state_transition(states + 26, states + 32, '0', '0', 'R');
	add_state_transition(states + 26, states + 32, '1', '1', 'R');
	add_state_transition(states + 26, states + 32, ' ', ' ', 'R');
	add_state_transition(states + 32, states + 37, 'A', '0', 'R');
	add_state_transition(states + 32, states + 37, 'B', '0', 'R');

	add_state_transition(states + 24, states + 34, '1', ' ', 'L');
	add_state_transition(states + 34, states + 34, '0', '0', 'L');
	add_state_transition(states + 34, states + 34, '1', '1', 'L');
	add_state_transition(states + 34, states + 34, 'A', '0', 'L');
	add_state_transition(states + 34, states + 34, 'B', '1', 'L');
	add_state_transition(states + 34, states + 35, '#', '#', 'L');
	add_state_transition(states + 34, states + 34, '$', '$', 'L');
	add_state_transition(states + 35, states + 35, 'A', 'A', 'L');
	add_state_transition(states + 35, states + 35, 'B', 'B', 'L');
	add_state_transition(states + 35, states + 36, '0', '0', 'R');
	add_state_transition(states + 35, states + 36, '1', '1', 'R');
	add_state_transition(states + 35, states + 36, ' ', ' ', 'R');
	add_state_transition(states + 36, states + 37, 'A', '1', 'R');
	add_state_transition(states + 36, states + 37, 'B', '1', 'R');

	add_state_transition(states + 37, states + 37, 'A', 'A', 'R');
	add_state_transition(states + 37, states + 37, 'B', 'B', 'R');
	add_state_transition(states + 37, states + 37, '#', '#', 'R');
	add_state_transition(states + 37, states + 37, '0', '0', 'R');
	add_state_transition(states + 37, states + 37, '1', '1', 'R');
	add_state_transition(states + 37, states + 38, '$', '$', 'R');
	add_state_transition(states + 38, states + 38, '0', '0', 'R');
	add_state_transition(states + 38, states + 38, '1', '1', 'R');
	add_state_transition(states + 38, states + 24, ' ', ' ', 'L');
	add_state_transition(states + 24, states + 41, '$', '$', 'L'); //go to reset B.
	
	add_state_transition(states + 39, states + 40, '#', ' ', 'L');
	add_state_transition(states + 39, states + 39, '$', ' ', 'L');
	add_state_transition(states + 39, states + 39, 'A', ' ', 'L');
	add_state_transition(states + 39, states + 39, 'B', ' ', 'L');
	add_state_transition(states + 39, states + 39, '1', ' ', 'L');
	add_state_transition(states + 39, states + 39, '0', ' ', 'L');
	add_state_transition(states + 40, states + 40, 'A', '0', 'L');
	add_state_transition(states + 40, states + 40, 'B', '1', 'L');
	add_state_transition(states + 40, NULL, ' ',' ','R');

	add_state_transition(states + 41, states + 41, 'A', '0', 'L');
	add_state_transition(states + 41, states + 41, 'B', '1', 'L');
	add_state_transition(states + 41, states + 41, '#', '#', 'L');
	add_state_transition(states + 41, states + 41, '1', '1', 'L');
	add_state_transition(states + 41, states + 41, '0', '0', 'L');
	add_state_transition(states + 41, states, ' ', ' ', 'R');
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
}

void solve_mod(TM* tm) {
	add_terminate_sym(tm, '$');
	pad_inputs(tm, '#', '$');
	add_terminate_sym(tm, '#');
	pad_inputs(tm, '$', '#');
	add_terminate_sym(tm, '$');
	find_remainder(tm);
	print_tape(tm->tape_head);
}

int main() {
	TM calc_remainder;
	char input[MAXLEN];
	scanf("%s", input);
	initalize_TM(input, &calc_remainder);
	solve_mod(&calc_remainder);
}