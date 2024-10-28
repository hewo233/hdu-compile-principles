import nfa_part

def build_nfa_from_postfix(postfix_expr):
    stack = []
    for char in postfix_expr:
        if char.isalnum():  # 是操作数，构建单个符号的NFA
            stack.append(nfa_part.build_nfa_single_symbol(char))
        elif char == '.':  # 连接操作
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(nfa_part.concat_nfa(nfa1, nfa2))
        elif char == '|':  # 并联操作
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(nfa_part.parallel_nfa(nfa1, nfa2))
        elif char == '*':  # 闭包操作
            nfa = stack.pop()
            stack.append(nfa_part.kleene_star_nfa(nfa))

    return stack.pop()  # 最后堆栈中剩下的NFA是完整的NFA
