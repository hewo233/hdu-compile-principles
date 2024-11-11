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
    # epsilon 闭包
    stack = list(states)  
    closure = set(states)  
    while stack:
        state = stack.pop()
        
        if 'ε' in nfa.transitions[state]:
            for next_state in nfa.transitions[state]['ε']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure
