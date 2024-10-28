def add_explicit_concat_operator(expression): 
    # 添加显式连接操作符
    output = []
    operators = {'*', '|', '(', ')'}
    for i in range(len(expression) - 1):
        output.append(expression[i])
        # 如果当前字符是操作数或闭包操作后，下一个字符是操作数或'('，则需要加'.'
        if (expression[i].isalnum() or expression[i] == '*') and \
           (expression[i+1].isalnum() or expression[i+1] == '('):
            output.append('.')
    output.append(expression[-1])
    return ''.join(output)

def infix_to_postfix(expression):
    precedence = {'*': 3, '.': 2, '|': 1}  # '.' 表示连接操作
    stack = []
    output = []
    for char in expression:
        if char.isalnum():  # 操作数直接输出
            output.append(char)
        elif char == '(':  # '(' 入栈
            stack.append(char)
        elif char == ')':  # ')' 弹栈直到遇到 '('
            top_token = stack.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = stack.pop()
        else:  # 运算符
            while (stack and stack[-1] != '(' and
                   precedence[stack[-1]] >= precedence[char]):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())
    return ''.join(output)

