from email import header


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description       :Filters out the sensitive words in the text.
@Date     :2022/08/27 10:02:23
@Author      :Lv Chuancheng
@version      :1.0
'''

import time
from opencc import OpenCC

BLACK_WORD_PATH = './source/black_words.txt'
STOP_WORD_PATH = './source/stop_words.txt'


class DFAFilter(object):
    """基于DFA算法的敏感词过滤系统

    存储敏感词表并对指定文本段进行多种匹配，包括：
    1. 完全匹配
    2. 过滤停顿词后的匹配
    3. 繁简体转换后的匹配
    4. 单字重复的匹配

    Attributes:
        black_words: 敏感词表
        stop_words: 停顿词表
        black_word_chains: 敏感词链表
        delimit: 中止符
    """

    def __init__(self):
        super(DFAFilter, self).__init__()
        self.black_words = self.read_file(BLACK_WORD_PATH)
        self.stop_words = self.read_file(STOP_WORD_PATH)
        self.black_word_chains = {}
        self.delimit = '\x00'
        self.parse_sensitive_words()

    def read_file(self, path):
        return [i.strip() for i in open(path, 'r', encoding='utf-8').readlines()]

    def parse_sensitive_words(self):
        for black_word in self.black_words:
            self.add_sensitive_words(black_word)

    def add_sensitive_words(self, black_word):
        black_word = black_word.lower()
        chars = black_word.strip()
        if not chars:
            return
        level = self.black_word_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
            if i == len(chars) - 1:
                level[self.delimit] = 0

    # 过滤敏感词
    def filter_sensitive_words(self, content, replace="*", t2s=True):
        """对指定文本进行过滤
        
        Args:
            content: 文本内容
            replace: 替换的字符，默认为"*"
            t2s: 是否繁体转简体，默认为True。开启后，将字符转换为简体，效率大幅度降低。

        Returns:
            过滤后的文本，如果有敏感词，则替换为replace
            过滤的敏感词列表
        """
        
        
        filterd_content = ''
        black_words = []
        idx = 0
        while idx < len(content):
            level = self.black_word_chains
            step_ins = 0
            message_chars = content[idx:]
            black_word = ''
            last_char = ''
            for char in message_chars:
                simp_char = OpenCC('t2s').convert(char) if t2s else char
                if simp_char in self.stop_words or char == last_char:
                    step_ins += 1
                    continue
                last_char = char
                if simp_char in level:
                    step_ins += 1
                    black_word += char
                    if self.delimit not in level[simp_char]:
                        level = level[simp_char]
                    else:
                        black_words.append(black_word)
                        black_word = ''
                        filterd_content += replace * step_ins
                        idx += step_ins - 1
                        break
                else:
                    filterd_content += content[idx]
                    black_word = ''
                    break
            if len(black_word) != 0:
                filterd_content += content[idx]
            idx += 1
        return filterd_content, black_words


if __name__ == "__main__":
    dfa_filter = DFAFilter()
    while True:
        content = input('请输入要过滤的内容(q for quit)：')
        if content == 'q':
            break
        start_time = time.time()
        filtered_content, black_words = dfa_filter.filter_sensitive_words(
            content)
        end_time = time.time()
        print("过滤后的内容：", filtered_content)
        print("敏感词：", black_words)
        print('总共耗时：' + str(end_time - start_time) + 's')
