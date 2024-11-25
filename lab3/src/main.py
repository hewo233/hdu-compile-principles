from handle.cfg import CFG

def main():
    cfg = CFG(read=True)

    print("\n原始:")
    cfg.display()

    ## 消除左递归和提取左公因子
    cfg.eliminate_left_recursion()
    cfg.extract_left_common_factors()

    ## 计算First集和Follow集
    cfg.compute_firstSets()
    cfg.compute_followSets()

    print("\n处理后:")
    cfg.display()

    print("满足LL(1):", cfg.is_ll1())

    ## 构造预测分析表
    cfg.construct_predictive_table()

    while True:
        try:
            inputStr = input("输入待分析串:").strip()
            if inputStr:
                print(f"\033[32m已获取输入串: '{inputStr}'\033[0m")
                print(f"分析结果: {cfg.parse(inputStr.split(" "))}")
        except EOFError:
            break


if __name__ == "__main__":
    main()
