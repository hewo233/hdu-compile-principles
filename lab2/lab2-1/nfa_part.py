class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

class NFA:
    def __init__(self, start_state=None):
        self.start_state = start_state
        self.states = set()

    def add_state(self, state):
        self.states.add(state)

def build_nfa_single_symbol(symbol):
    start = State()
    end = State(is_final=True)
    start.add_transition(symbol, end)
    nfa = NFA(start)
    nfa.add_state(start)
    nfa.add_state(end)
    return nfa

def concat_nfa(first_nfa, second_nfa):
    for state in first_nfa.states:
        if state.is_final:
            state.is_final = False  # 第一个NFA的接受状态不再是接受状态
            for symbol, states in second_nfa.start_state.transitions.items():
                for s in states:
                    state.add_transition(symbol, s)

    first_nfa.states.update(second_nfa.states)
    return first_nfa

def parallel_nfa(first_nfa, second_nfa):
    start = State()  # 新的起始状态
    end = State(is_final=True)  # 新的接受状态
    start.add_transition('ε', first_nfa.start_state)
    start.add_transition('ε', second_nfa.start_state)
    
    # 将所有原始接受状态的转移指向新的接受状态
    for state in first_nfa.states.union(second_nfa.states):
        if state.is_final:
            state.is_final = False
            state.add_transition('ε', end)

    new_nfa = NFA(start)
    new_nfa.states = first_nfa.states.union(second_nfa.states, {start, end})
    return new_nfa

def kleene_star_nfa(nfa):
    start = State()  # 新的起始状态
    end = State(is_final=True)  # 新的接受状态
    start.add_transition('ε', nfa.start_state)
    start.add_transition('ε', end)
    
    # 所有原始接受状态现在通过ε转移回原始起始状态和新的接受状态
    for state in nfa.states:
        if state.is_final:
            state.is_final = False
            state.add_transition('ε', end)
            state.add_transition('ε', nfa.start_state)

    kleene_nfa = NFA(start)
    kleene_nfa.states = nfa.states.union({start, end})
    return kleene_nfa

