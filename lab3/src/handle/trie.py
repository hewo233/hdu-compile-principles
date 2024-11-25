class TrieNode:
    def __init__(self, isEnd: bool = False):
        self.children: dict[str, TrieNode] = {}
        self.isEnd: bool = isEnd

    def find_child(self, symbal: str) -> "TrieNode":
        return self.children.get(symbal)


class Trie:
    def __init__(self, rootSym: str):
        self.rootSym: str = rootSym
        self.rootNode: TrieNode = TrieNode()

    # 插入一个字符串
    def insert(self, symbals: list[str]) -> None:
        curNode = self.rootNode
        for sym in symbals:
            childNode = curNode.find_child(sym)
            if childNode:
                curNode = childNode
            else:
                newNode = TrieNode()
                curNode.children[sym] = newNode
                curNode = newNode
        curNode.isEnd = True

    # 前缀路径
    def get_prefixes(self) -> list[list[str]]:
        def get_prefix(symbal: str, node: TrieNode) -> list[str]:
            prefix = [symbal]
            curNode = node
            while len(curNode.children) == 1 and not curNode.isEnd:
                childSym, childNode = next(iter(curNode.children.items()))
                prefix.append(childSym)  # 添加到前缀
                curNode = childNode
            return prefix if len(curNode.children) > 1 else None

        # 遍历根节点的所有子节点
        prefixes: list[list[str]] = []
        for childSym, childNode in self.rootNode.children.items():
            prefix = get_prefix(childSym, childNode)
            if prefix:
                prefixes.append(prefix)

        return prefixes

    def display(self) -> None:
        def display_help(symbal: str, node: TrieNode, prefix: str, last: bool) -> None:
            print(prefix + "-" + symbal)
            newPrefix = prefix if not last else prefix[:-1] + " "
            newPrefix += len(symbal) * " " + "|"
            childPeers = len(node.children)
            children = iter(node.children.items())
            for i in range(childPeers):
                childSym, childNode = next(children)
                display_help(childSym, childNode, newPrefix, i == childPeers - 1)

        print(self.rootSym)
        prefix = (len(self.rootSym) - 1) * " " + "|"
        peers = len(self.rootNode.children)
        children = iter(self.rootNode.children.items())
        for i in range(peers):
            childSym, childNode = next(children)
            display_help(childSym, childNode, prefix, i == peers - 1)

