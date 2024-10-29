class NFA:
    def __init__(self, states, transitions, initial_state, accept_states):
        self.states = states  # 所有状态的集合
        self.transitions = transitions  # 转换关系，格式为 {state: {symbol: set(states)}}
        self.initial_state = initial_state  # 初始状态
        self.accept_states = accept_states  # 接受状态集合

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = set()
        self.transitions[from_state][symbol].add(to_state)

def epsilon_closure(nfa, states):
    """ 计算给定状态集的ε-闭包 """
    stack = list(states)  # 初始化栈
    closure = set(states)  # ε-闭包最初包含给定的状态集
    while stack:
        state = stack.pop()
        # 检查当前状态是否有ε转换
        if 'ε' in nfa.transitions[state]:
            for next_state in nfa.transitions[state]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure

class DFA:
    def __init__(self, initial_state):
        self.states = set()  # DFA的状态集合
        self.transitions = {}  # DFA的转换表
        self.initial_state = initial_state  # DFA的初始状态
        self.accept_states = set()  # DFA的接受状态集合

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, from_state, input_symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][input_symbol] = to_state

    def add_accept_state(self, state):
        self.accept_states.add(state)

    def __str__(self):
        return f'States: {self.states}\nTransitions: {self.transitions}\n' \
               f'Initial State: {self.initial_state}\nAccept States: {self.accept_states}'

def subset_construction(nfa):
    input_symbols = {sym for state in nfa.transitions for sym in nfa.transitions[state] if sym != 'ε'}

    initial_closure = epsilon_closure(nfa, {nfa.initial_state})
    initial_state = frozenset(initial_closure)
    dfa = DFA(initial_state=initial_state)
    dfa.add_state(initial_state)
    
    # 初始状态是否是接受状态
    if nfa.accept_states.intersection(initial_closure):
        dfa.add_accept_state(initial_state)

    worklist = [initial_state]
    marked_states = set(worklist)

    while worklist:
        current = worklist.pop()
        for symbol in input_symbols:

            next_states = set()

            for state in current:
                if symbol in nfa.transitions.get(state, {}):
                    next_states.update(nfa.transitions[state][symbol])

            next_closure = frozenset(epsilon_closure(nfa, next_states))

            if next_closure not in marked_states:
                marked_states.add(next_closure)
                worklist.append(next_closure)
                dfa.add_state(next_closure)
                if nfa.accept_states.intersection(next_closure):
                    dfa.add_accept_state(next_closure)

            dfa.add_transition(current, symbol, next_closure)

    return dfa

