import nfa_all
import sim
import trans

def test_nfa():
    regex = "a(b|c)*"
    print(f"testing regex: {regex}")
    processed_regex = trans.add_explicit_concat_operator(regex)
    postfix_regex = trans.infix_to_postfix(processed_regex)
    print(f"postfix regex: {postfix_regex}")
    nfa = nfa_all.build_nfa_from_postfix(postfix_regex)

    test_strings = ["abcbcbc", "accccc", "abbbb", "a", "abc", "bbc"]
    for s in test_strings:
        result = sim.simulate_nfa(nfa, s)
        print(f"Input: {s}, Accepted: {result}")

test_nfa()
