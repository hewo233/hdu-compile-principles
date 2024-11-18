def simulate_dfa(dfa, input_string):
    current_state = dfa.initial_state
    for symbol in input_string:
        if symbol in dfa.transitions.get(current_state, {}):
            current_state = dfa.transitions[current_state][symbol]
        else:
            return False 
    return current_state in dfa.accept_states

