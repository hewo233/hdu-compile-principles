def simulate_nfa(nfa, input_string):
    current_states = set()
    # 初始化当前状态包括起始状态及其通过ε转移可达的所有状态
    add_epsilon_transitions(current_states, nfa.start_state)

    for char in input_string:
        next_states = set()
        for state in current_states:
            if char in state.transitions:
                for next_state in state.transitions[char]:
                    add_epsilon_transitions(next_states, next_state)
        current_states = next_states

    # 检查是否有任何当前状态是接受状态
    return any(state.is_final for state in current_states)

def add_epsilon_transitions(state_set, state):
    if state not in state_set:
        state_set.add(state)
        if 'ε' in state.transitions:
            for next_state in state.transitions['ε']:
                add_epsilon_transitions(state_set, next_state)
