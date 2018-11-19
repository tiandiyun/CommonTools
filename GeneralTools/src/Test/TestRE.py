# -*- coding:utf8 -*-

import re


def TestMatch():
    #m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!!!')
    m = re.match(r'(\w+) (\w+)(?P<sign>\W*)(\1)', 'hello world!!!hello')

    print("m.string:", m.string)
    print("m.re:", m.re)
    print("m.pos:", m.pos)
    print("m.endpos:", m.endpos)
    print("m.lastindex:", m.lastindex)
    print("m.lastgroup:", m.lastgroup)

    print("m.group(1,2):", m.group(1, 2))
    print("m.groups():", m.groups())
    print("m.groupdict():", m.groupdict())
    print("m.start(2):", m.start(2))
    print("m.end(2):", m.end(2))
    print("m.span(2):", m.span(2))
    print(r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3'))
    print("m.span(2):", m.span(2))
    print(r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3'))

    ### output ###
    # m.string: hello world!
    # m.re: <_sre.SRE_Pattern object at 0x016E1A38>
    # m.pos: 0
    # m.endpos: 12
    # m.lastindex: 3
    # m.lastgroup: sign
    # m.group(1,2): ('hello', 'world')
    # m.groups(): ('hello', 'world', '!')
    # m.groupdict(): {'sign': '!'}
    # m.start(2): 6
    # m.end(2): 11
    # m.span(2): (6, 11)
    # m.expand(r'\2 \1\3'): world hello!

def TestSub():
    p = re.compile(r'(\w+) (\w+)')
    s = 'i say, hello world!'

    s0 = p.search(s)
    print(s0.groups())

    s_size = len(s0.groups())
    for i in range(s_size):
        print(s0.group(i + 1))

    s1 = p.sub(r'\2 \1', s)

    def func(m):
        return m.group(1).title() + ' ' + m.group(2).title()

    s2 = p.sub(func, s)

    inputStr = "hello crifan, nihao crifan"
    replacedStr = re.sub(r"hello (\w+), nihao (\1)", r"\1", inputStr)
    print("replacedStr=", replacedStr)  # crifan


if __name__ == "__main__":
    # p = re.compile(r'(\b\w+)\s+\1')
    # rslt = p.search('Paris in the the spring').group()
    #
    # grp = re.search(r'(\b\w+)\s+\1', 'Paris in the the spring')
    #
    # print(rslt)
    # exit()

    TestMatch()