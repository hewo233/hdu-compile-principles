from .trie import *


class CFG:
    def __init__(self, read=False):
        self.terminalSyms: set[str] = set()  # 终结符号集
        self.startSym: str = None  # 开始符号
        self.grammar: dict[str, list[list[str]]] = {}  # 产生式
        self.firstSets: dict[str, set[str]] = {}  # FIRST 集
        self.followSets: dict[str, set[str]] = {}  # FOLLOW 集
        self.predictiveTable: dict[str, dict[str, list[list[str]]]] = {}  # 预测分析表

        if read:
            self.read_grammar()

    def read_grammar(self) -> None:
        """读取文法"""
        symbal: set[str] = set()
        while True:
            try:
                self.startSym = input("请输入文法开始符号: ").strip()  # 获取开始符号
                assert len(self.startSym) == 1
                break
            except AssertionError:
                print("\033[31m上下文无关语法有且仅有一个开始符号\033[0m")
        symbal.add(self.startSym)
        print(f"\033[32m已读取开始符号: '{self.startSym}'\033[0m")

        print("请输入文法（使用 'END' 来结束输入）: ")
        while True:
            try:
                line = input()
            except EOFError:
                break

            if line.strip().upper() == "END":
                break
            if "->" in line:
                non_terminal, productions = line.split("->")
                non_terminal = non_terminal.strip()
                try:
                    assert len(self.startSym) == 1
                except AssertionError:
                    print("\033[31m上下文无关语法产生式左侧只能有一个非总结符号\033[0m")
                productions = [prod.split() for prod in productions.split("|")]
                print(
                    f"\033[32m已读取产生式: {non_terminal} -> {" | ".join([" ".join(prod) for prod in productions])}\033[0m"
                )
                self.add_rule(non_terminal, productions)

    def set_start(self, startSym: str) -> None:
        """设置文法开始符号"""
        self.startSym = startSym

    def add_rule(self, nonterminalSym: str, productions: list[list[str]]) -> None:
        """添加产生式规则, 根据规则判断终结符号和非终结符号"""
        if nonterminalSym not in self.grammar:
            self.grammar[nonterminalSym] = productions
        else:
            self.grammar[nonterminalSym] += productions

        if nonterminalSym in self.terminalSyms:
            self.terminalSyms.remove(nonterminalSym)
        self.terminalSyms.update(
            sym
            for production in productions
            for sym in production
            if sym not in self.grammar
        )

    def eliminate_left_recursion(self) -> None:
        """消除左递归的函数"""
        nonterminalSyms = list(self.grammar.keys())

        # 按顺序处理每个非终结符号
        for i in range(len(nonterminalSyms)):
            nonterminalSym = nonterminalSyms[i]
            productions = self.grammar[nonterminalSym]

            nonrecursiveProductions: list[list[str]] = []
            recursiveProductions: list[list[str]] = []

            # 消除间接左递归, 遍历在当前非终结符号之前的所有非终结符号
            for j in range(i):
                # 对当前非终结符号的每个产生式进行检查
                for prod in productions.copy():
                    # Ai -> Ajβ
                    if prod[0] == nonterminalSyms[j]:
                        productions.remove(prod)
                        productions.extend(
                            [
                                prodj + prod[1:]
                                for prodj in self.grammar[nonterminalSyms[j]]
                            ]
                        )

            for newProd in productions:
                if newProd[0] == nonterminalSym:
                    recursiveProductions.append(newProd[1:])
                else:
                    nonrecursiveProductions.append(newProd)

            # 处理直接左递归
            if recursiveProductions:
                newNonterminalSym = f"{nonterminalSym}'"
                for prod in nonrecursiveProductions:
                    prod.append(newNonterminalSym)
                self.grammar[nonterminalSym] = nonrecursiveProductions
                for prod in recursiveProductions:
                    prod.append(newNonterminalSym)
                recursiveProductions.append(["ε"])
                self.add_rule(newNonterminalSym, recursiveProductions)
            else:
                self.grammar[nonterminalSym] = nonrecursiveProductions

    def extract_left_common_factors(self):
        """提取左公因式"""
        newGrammar: dict[str, list[list[str]]] = {key: [] for key in self.grammar}

        for nonterminalSym, productions in self.grammar.items():
            # 如果产生式右部符号个数≤1, 直接赋值
            if len(productions) <= 1:
                newGrammar[nonterminalSym] = productions
                continue

            # 将产生式加入到 Trie 中
            trie = Trie(nonterminalSym)
            for prod in productions:
                trie.insert(prod)

            # 获取最长公共因子式
            commonPrefixes = trie.get_prefixes()

            if commonPrefixes:
                newNonterminalSym = nonterminalSym
                prefixMap: list[tuple[list[str], str]] = []
                # 根据前缀构造新规则
                for commonPrefix in commonPrefixes:
                    newNonterminalSym = f"{newNonterminalSym}'" 
                    prefixMap.append((commonPrefix, newNonterminalSym))
                    newGrammar[newNonterminalSym] = []
                    newGrammar[nonterminalSym].append(
                        commonPrefix + [newNonterminalSym]
                    )
                
                # 分配规则到新非终结符
                for prod in productions:
                    for commonPrefix, newNonterminalSym in prefixMap:
                        commonPrefixLen = len(commonPrefix)
                        if prod[:commonPrefixLen] == commonPrefix:
                            newGrammar[newNonterminalSym].append(prod[commonPrefixLen:])
                            break
                    else:
                        newGrammar[nonterminalSym].append(prod)
            else:
                newGrammar[nonterminalSym] = productions

        self.grammar = newGrammar

    #递归计算FIRST集
    def compute_first(self, symbol: str) -> set[str]:
        if not self.firstSets:
            self.compute_firstSets()

        # 如果是终结符号，直接返回
        if symbol not in self.firstSets:
            return {symbol}
        
        # 如果已经计算过，直接返回
        if self.firstSets[symbol]:
            return self.firstSets[symbol]
        
        # 计算 FIRST 集
        for prod in self.grammar[symbol]:
            count = 0
            for prodSym in prod:
                symFirst = self.compute_first(prodSym)
                if "ε" not in symFirst:
                    self.firstSets[symbol].update(symFirst)
                    break
                count += 1
                self.firstSets[symbol].update(symFirst - {"ε"})
            if count == len(prod):
                self.firstSets[symbol].add("ε")

        return self.firstSets[symbol]

    def compute_first_of_production(self, production: list[str]) -> set[str]:
        firstSet: set[str] = set()
        for symbol in production:
            first = self.compute_first(symbol)
            if "ε" not in first:
                firstSet.update(first)
                break
            elif symbol == production[-1]:
                firstSet.update(first)
            else:
                firstSet.update(first - {"ε"})

        return firstSet

    def compute_firstSets(self) -> dict[str, set[str]]:
        """计算 FIRST 集"""
        if self.firstSets:
            return self.firstSets

        # 初始化
        for nonterminalSym in self.grammar.keys():
            self.firstSets[nonterminalSym] = set()

        # 遍历每个非终结 计算 FIRST 集
        for nonterminalSym in self.firstSets.keys():
            self.compute_first(nonterminalSym)

        return self.firstSets

    def compute_follow(self, symbol: str) -> set[str]:
        if not self.followSets:
            self.compute_followSets()
        return self.followSets[symbol]

    def compute_followSets(self) -> dict[str, set[str]]:
        """计算 FOLLOW 集"""
        if self.followSets:
            return self.followSets

        # 初始化所有非终结符的 FOLLOW 集
        for nonterminal in self.grammar.keys():
            self.followSets[nonterminal] = set()
        self.followSets[self.startSym].add("$")  # $ 为输入的结束符

        # 迭代直到所有 FOLLOW 集不再变化
        changed = True
        while changed:
            changed = False
            for nonterminal, productions in self.grammar.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol not in self.terminalSyms:  # 当前符号是非终结符
                            originalSize = len(self.followSets[symbol])

                            if i + 1 < len(production):  # 右侧还有符号
                                firstSet = self.compute_first_of_production(
                                    production[i + 1 :]
                                )
                                self.followSets[symbol].update(firstSet - {"ε"})
                                if "ε" in firstSet:
                                    self.followSets[symbol].update(
                                        self.followSets[nonterminal]
                                    )
                            else:  # 如果是最后一个符号，添加非终结符的 FOLLOW 集
                                self.followSets[symbol].update(
                                    self.followSets[nonterminal]
                                )

                            changed |= originalSize != len(self.followSets[symbol])

        return self.followSets

    def compute_select_of_production(
        self, nonterminalSym: str, production: list[str]
    ) -> set[str]:
        """计算某个产生式的 SELECT 集"""
        selectSet: set[str] = set()

        # 计算产生式右部的 FIRST 集
        firstSet = self.compute_first_of_production(production)

        # 将 FIRST 集中除 ε 之外的符号加入 SELECT 集
        selectSet.update(firstSet - {"ε"})

        # 如果在里面，再加个 FOLLOW（A）
        if "ε" in firstSet:
            selectSet.update(self.compute_follow(nonterminalSym))

        return selectSet

    def is_ll1(self) -> bool:
        """判断文法是否是 LL(1) 文法"""
        # 遍历所有非终结符及其产生式
        for nonterminalSym, productions in self.grammar.items():
            if len(productions) <= 1:
                continue

            selectSets = []

            # 计算所有产生式的 SELECT 集
            for production in productions:
                newSelectSet = self.compute_select_of_production(nonterminalSym, production)
                selectSets.append(newSelectSet)

            # 检查所有 SELECT 集之间是否有交集
            for i in range(len(selectSets)):
                for j in range(i + 1, len(selectSets)):
                    if selectSets[i].intersection(selectSets[j]):
                        return False

        return True

    def construct_predictive_table(self) -> dict[str, dict[str, list[list[str]]]]:
        """构造 LL(1) 预测分析表"""
        self.predictiveTable = {
            nonterminal: {terminal: [] for terminal in self.terminalSyms | {"$"}}
            for nonterminal in self.grammar.keys()
        }

        #遍历所有非终结符及其产生式
        for nonterminal, productions in self.grammar.items():
            for prod in productions:
                selectSet = self.compute_select_of_production(nonterminal, prod)

                # 给 每个 SELECT 填进去
                for terminal in selectSet:
                    self.predictiveTable[nonterminal][terminal].append(prod)

        return self.predictiveTable

    def parse(self, inputStr: list[str]) -> bool:
        if not self.predictiveTable:
            self.construct_predictive_table()
        if not self.is_ll1():
            print("\033[31m该文法不是LL(1)文法\033[0m")
            return False

        
        stack: list[str] = ["$", self.startSym]
        print("初始分析栈:", stack)

        inputStr.append("$")
        while stack:
            top = stack.pop()
            curSym = inputStr[0]
            action: str = None

            # 判断栈顶是终结符号
            if top in self.terminalSyms | {"$"}:
                if top == curSym:
                    # 匹配
                    action = f"match: '{curSym}'"
                    inputStr = inputStr[1:]
                else:
                    return False
            else:
                # 预测分析表中找到对应的产生式
                productions = self.predictiveTable[top][curSym]
                if productions:
                    production = productions[0]
                    # 将产生式的符号逆序入栈
                    for sym in reversed(production):
                        if sym != "ε":
                            stack.append(sym)
                    action = f"{top} -> {" ".join(production)}"
                else:
                    return False

            print(f"分析栈: {list(reversed(stack))}, 输入串: '{" ".join(inputStr)}', 动作: {action}")

        return True

    def display(self):
        print(f"开始符号: '{self.startSym}'")
        print(f"非终结符号集: [{", ".join(self.grammar.keys())}]")
        print(f"终结符号集: [{", ".join(self.terminalSyms)}]")
        print("产生式:")
        for nonterminalSym in self.grammar:
            productions = " | ".join(
                [" ".join(production) for production in self.grammar[nonterminalSym]]
            )
            print(f"{nonterminalSym} -> {productions}")

        if self.firstSets:
            print("FIRST 集:")
            for nonterminal in self.firstSets:
                print(
                    f"FIRST({nonterminal}) = {{{', '.join(self.firstSets[nonterminal])}}}"
                )

        if self.followSets:
            print("FOLLOW 集:")
            for nonterminal in self.followSets:
                print(
                    f"FOLLOW({nonterminal}) = {{{', '.join(self.followSets[nonterminal])}}}"
                )

        if self.predictiveTable:
            print("预测分析表:")
            for nonterminal, rules in self.predictiveTable.items():
                print(f"{nonterminal}:")
                for terminal, productions in rules.items():
                    if len(productions):
                        print(f"\t{terminal}:")
                    for prod in productions:
                        print(f"\t\t{nonterminal} -> {" ".join(prod)}")
