#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define MAXLEN 4096
#define SYMBOLS 6

int num_states = 0;
int step_counter = 0;
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

void remove_n(TM* tm) {
	int nstate = 3;
	state states[nstate];
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	add_state_transition(states, states, '0', ' ', 'R');
	add_state_transition(states, states, '1', ' ', 'R');
	add_state_transition(states, states + 1, '#', ' ', 'R');
	add_state_transition(states + 1, states + 1, '0', '0', 'R');
	add_state_transition(states + 1, states + 1, '1', '1', 'R');
	add_state_transition(states + 1, states + 1, '#', '#', 'R');
	add_state_transition(states + 1, states + 2, ' ', '$', 'L');
	add_state_transition(states + 2, states + 2, '0', '0', 'L');
	add_state_transition(states + 2, states + 2, '1', '1', 'L');
	add_state_transition(states + 2, states + 2, '#', '#', 'L');
	add_state_transition(states + 2, NULL, ' ', ' ', 'R');
	state* cur_state = states;
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
}

void max_degree(TM* tm) {
	// printf("%s", tm->tape_head);
	int nstate = 6;
	state states[nstate];
	for(int i = 0; i < nstate; ++i) create_state(states + i);
	add_state_transition(states, states, '0', '0', 'R');
	add_state_transition(states, states + 1, '1', 'A', 'R');
	add_state_transition(states, states, '#', '#', 'R');
	add_state_transition(states, NULL, '$', '$', 'R');
	add_state_transition(states, states, 'A', 'A', 'R');
	add_state_transition(states + 1, states + 1, '0', '0', 'R');
	add_state_transition(states + 1, states + 1, '1', '1', 'R');
	add_state_transition(states + 1, states + 2, '#', '#', 'R');
	add_state_transition(states + 2, states + 2, '0', '0', 'R');
	add_state_transition(states + 2, states + 3, '1', 'A', 'R');
	add_state_transition(states + 2, states + 2, '#', '#', 'R');
	add_state_transition(states + 2, states + 4, '$', '$', 'R');
	add_state_transition(states + 2, states + 2, 'A', 'A', 'R');
	add_state_transition(states + 3, states + 3, '0', '0', 'R');
	add_state_transition(states + 3, states + 3, '1', '1', 'R');
	add_state_transition(states + 3, states + 2, '#', '#', 'R');
	add_state_transition(states + 4, states + 4, '1', '1', 'R');
	add_state_transition(states + 4, states + 5, ' ', '1', 'L');
	add_state_transition(states + 5, states + 5, '0', '0', 'L');
	add_state_transition(states + 5, states + 5, '1', '1', 'L');
	add_state_transition(states + 5, states + 5, '#', '#', 'L');
	add_state_transition(states + 5, states + 5, '$', '$', 'L');
	add_state_transition(states + 5, states + 5, 'A', 'A', 'L');
	add_state_transition(states + 5, states, ' ', ' ', 'R');
	state* cur_state = states;
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
}

void convert_to_binary(TM* tm) {
	int nstate = 4;
	state states[nstate];
	if (tm->tape_head[0] == ' ') return;
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	// add_state_transition(states, NULL, ' ', ' ', 'R');
	add_state_transition(states, states + 1, '1', '#', 'L');
	add_state_transition(states, states + 2, ' ', ' ', 'L');
	add_state_transition(states, states, '#', '#', 'R');
	add_state_transition(states, states, '0', '0', 'R');
	add_state_transition(states + 1, states + 1, '1', '0', 'L');
	add_state_transition(states + 1, states, ' ', '1', 'R');
	add_state_transition(states + 1, states + 1, '#', '#', 'L');
	add_state_transition(states + 1, states, '0', '1', 'R');
	add_state_transition(states + 2, states + 2, '#', ' ', 'L');
	add_state_transition(states + 2, states + 3, '1', '1', 'L');
	add_state_transition(states + 2, states + 3, '0', '0', 'L');
	add_state_transition(states + 3, states + 3, '1', '1', 'L');
	add_state_transition(states + 3, states + 3, '0', '0', 'L');
	add_state_transition(states + 3, NULL, ' ', ' ', 'R');
	state* cur_state = states;
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
}

void clear_prev(TM* tm) {
	int nstate = 3;
	state states[nstate];
	for (int i = 0; i < nstate; ++i) create_state(states + i);
	add_state_transition(states, NULL, ' ', ' ', 'R');
	add_state_transition(states, states + 1, '1', '1', 'L');
	add_state_transition(states, states + 1, '0', '0', 'L');
	add_state_transition(states + 1, states + 1, '1', '$', 'L');
	add_state_transition(states + 1, states + 1, '0', '$', 'L');
	add_state_transition(states + 1, states + 1, '#', '$', 'L');
	add_state_transition(states + 1, states + 1, '$', 'A', 'L');
	add_state_transition(states + 1, states + 1, 'A', '$', 'L');
	add_state_transition(states + 1, states + 2, ' ', ' ', 'R');
	add_state_transition(states + 2, states + 2, '$', ' ', 'R');
	add_state_transition(states + 2, NULL, 'A', ' ', 'R');
	state* cur_state = states;
	while (cur_state != NULL) {
		char input_sym = *tm->tape_head;
		cur_state = perform_state_transition(cur_state, input_sym, &tm->tape_head);
	}
}

void solve_max_degree(TM* find_max_degree) {
	remove_n(find_max_degree);
	max_degree(find_max_degree);
	clear_prev(find_max_degree);
	convert_to_binary(find_max_degree);
}

int main() {
	TM find_max_degree;
	char input[MAXLEN];
	scanf("%s", input);
	initalize_TM(input, &find_max_degree);
	solve_max_degree(&find_max_degree);
	print_tape(find_max_degree.tape_head);
}