import nfa_pre

class DFA:
    def __init__(self):
        self.states = set()  # DFA状态集
        self.transitions = {}  # DFA状态转换表
        self.initial_state = None  # DFA的初始状态
        self.accept_states = set()  # DFA的接受状态集合

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, from_state, symbol, to_state):
        from_state = frozenset(from_state) 
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state

    def set_initial_state(self, state):
        self.initial_state = state

    def add_accept_state(self, state):
        self.accept_states.add(state)

def nfa_to_dfa(nfa):
    initial_closure = nfa_pre.epsilon_closure(nfa, {nfa.initial_state})
    dfa = DFA()
    unmarked_states = [initial_closure]  # 未标记的DFA状态集合
    dfa.set_initial_state(frozenset(initial_closure))
    dfa.add_state(frozenset(initial_closure))

    while unmarked_states:
        current_dfa_state = unmarked_states.pop(0)
        # 获取所有符号
        for symbol in set(sym for state in current_dfa_state for sym in nfa.transitions.get(state, {})):
            if symbol == 'ε':
                continue
            
            new_state_set = set()

            for state in current_dfa_state:
                if symbol in nfa.transitions.get(state, {}):
                    new_state_set.update(nfa_pre.epsilon_closure(nfa, nfa.transitions[state][symbol]))
                    
            new_state_frozenset = frozenset(new_state_set)
            if new_state_frozenset not in dfa.states:
                dfa.add_state(new_state_frozenset)
                unmarked_states.append(new_state_frozenset)
                if any(s in nfa.accept_states for s in new_state_frozenset):
                    dfa.add_accept_state(new_state_frozenset)
            dfa.add_transition(current_dfa_state, symbol, new_state_frozenset)

    return dfa
