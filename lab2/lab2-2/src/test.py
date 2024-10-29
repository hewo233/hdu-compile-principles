import trans

def simulate_dfa(dfa, input_string):
    current_state = dfa.initial_state
    for symbol in input_string:
        if symbol in dfa.transitions[current_state]:
            current_state = dfa.transitions[current_state][symbol]
        else:
            return False  # 如果在当前状态没有对应的转换，则字符串被拒绝
    return current_state in dfa.accept_states  # 如果结束在接受状态，则字符串被接受


states = {'q0', 'q1', 'q2'}
transitions = {
    'q0': {'0': {'q0', 'q1'}, 'ε': {'q1'}},
    'q1': {'1': {'q2'}},
    'q2': {'0': {'q2'}}
}
initial_state = 'q0'
accept_states = {'q2'}

nfa = trans.NFA(states, transitions, initial_state, accept_states)

# 使用定义好的NFA进行子集构造，生成DFA
dfa = trans.subset_construction(nfa)

# 测试用例
test_cases = [
    ("000100", True),
    ("000110", True),
    ("001100", True),
    ("011000", False),  # 应被拒绝，因为从q1不能直接到q0
    ("000111", False),
    ("101010", False)
]

# 运行测试用例
for input_string, expected in test_cases:
    result = simulate_dfa(dfa, input_string)
    print(f"Testing input: {input_string}, Expected: {expected}, Got: {result}")

