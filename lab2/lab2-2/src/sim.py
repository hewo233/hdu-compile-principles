def simulate_dfa(dfa, input_string):
    current_state = dfa.initial_state
    for symbol in input_string:
        if symbol in dfa.transitions.get(current_state, {}):
            current_state = dfa.transitions[current_state][symbol]
        else:
            return False  # 输入中有不可识别的符号，导致无法转移状态
    return current_state in dfa.accept_states

