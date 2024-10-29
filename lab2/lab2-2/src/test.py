import nfa_pre
import dfa_trans
import sim

def test_nfa_to_dfa(nfa, test_cases):

    print("testing nfa_to_dfa...")

    # 将 NFA 转换为 DFA
    dfa = dfa_trans.nfa_to_dfa(nfa)

    # 执行测试
    results = []
    for input_string, expected in test_cases:
        # 模拟 DFA
        accepts = sim.simulate_dfa(dfa, input_string)
        results.append((input_string, accepts, expected))

    # 输出测试结果
    for result in results:
        print(f"string: {result[0]}, DFA: {result[1]}, expect: {result[2]}, test {'pass' if result[1] == result[2] else 'fail'}")

nfa1 = nfa_pre.NFA(
    states={'q0', 'q1', 'q2', 'q3'},
    transitions={
        'q0': {'a': {'q1'}},
        'q1': {'b': {'q2'}, 'a': {'q3'}},
        'q2': {'c': {'q3'}},
        'q3': {}
    },
    initial_state='q0',
    accept_states={'q3'}
)

test_cases1 = [
    ('abc', True),
    ('aab', False),
    ('ab', False),
    ('ac', False)
]

# a(b|c)*
nfa2 = nfa_pre.NFA(
    states={'q0', 'q1'},
    transitions={
        'q0': {'a': {'q1'}},
        'q1': {'b': {'q1'}, 'c': {'q1'}}
    },
    initial_state='q0',
    accept_states={'q1'}
)

test_cases2 = [
    ('a', True),
    ('ab', True),
    ('ac', True),
    ('abc', True),
    ('acb', True),
    ('abcbcbc', True),
    ('', False),   
    ('b', False),  
    ('ba', False)
]

nfa3 = nfa_pre.NFA(
    states=set(range(11)),
    transitions={
        'q0': {'ε': {'q1', 'q7'}},
        'q1': {'ε': {'q2', 'q4'}},
        'q2': {'a': {'q3'}},
        'q3': {'ε': {'q6'}},
        'q4': {'b': {'q5'}},
        'q5': {'ε': {'q6'}},
        'q6': {'ε': {'q7'}},
        'q7': {'a': {'q8'}},
        'q8': {'b': {'q9'}},
        'q9': {'b': {'q10'}},
        'q10': {}
    },
    initial_state='q0',
    accept_states={'q10'}
)

test_cases3 = [
    ('ab', False),
    ('abb', True),
    ('aabb', True),
    ('b', False),
    ('bb', False),
    ('bbb', False),
    ('aab', False),
    ('ba', False)
]


# 运行测试函数
test_nfa_to_dfa(nfa1, test_cases1)
test_nfa_to_dfa(nfa2, test_cases2)
test_nfa_to_dfa(nfa3, test_cases3)

