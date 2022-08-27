# SensitiveWordFilter

通过DFA算法实现敏感词过滤，可以过滤的敏感词包括：

1. 完全匹配敏感词（法轮功）
2. 匹配过滤停顿词后的敏感词（法@@!轮!　　功）
3. 匹配重复敏感词（法法法轮轮轮功功功）

资源包括：

1. black_words.txt: 敏感词列表
2. stop_words.txt: 停用词列表
