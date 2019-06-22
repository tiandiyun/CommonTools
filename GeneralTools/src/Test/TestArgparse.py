# -*- coding:utf8 -*-

import argparse

'''
add_argument() 方法定义如何解析命令行参数：

    原型 ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])

        name or flags - 选项字符串的名字或者列表，例如 foo 或者 -f, --foo。
        
        action - 命令行遇到参数时的动作，默认值是 store。
            store_const，表示赋值为const；
            append，将遇到的值存储成列表，也就是如果参数重复则会保存多个值;
            append_const，将参数规范中定义的一个值保存到一个列表；
            count，存储遇到的次数；此外，也可以继承 argparse.Action 自定义参数解析；
            
        nargs - 应该读取的命令行参数个数，可以是具体的数字，或者是?号，当不指定值时对于 Positional argument 使用 default，
            对于 Optional argument 使用 const；或者是 * 号，表示 0 或多个参数；或者是 + 号表示 1 或多个参数。
            
        const - action 和 nargs 所需要的常量值。
        
        default - 不指定参数时的默认值。
        
        type - 命令行参数应该被转换成的类型。
        
        choices - 参数可允许的值的一个容器。
        
        required - 可选参数是否可以省略 (仅针对可选参数)。
        
        help - 参数的帮助信息，当指定为 argparse.SUPPRESS 时表示不显示该参数的帮助信息.
        
        metavar - 在 usage 说明中的参数名称，对于必选参数默认就是参数名称，对于可选参数默认是全大写的参数名称.
        
        dest - 解析后的参数名称，默认情况下，对于可选参数选取最长的名称，中划线转换为下划线.
'''


def TestArgparse():

    '''定义了一个叫echo的参数，默认必选'''
    # parser = argparse.ArgumentParser()
    # parser.add_argument("echo")
    # args = parser.parse_args()
    # print(args.echo)


    '''
        可选参数，有两种方式：
            1. 通过一个-来指定的短参数，如-h；
            2. 通过--来指定的长参数，如--help
            
        parser.add_argument("-v", "--verbosity", help="increase output verbosity")
        定义了可选参数-v或--verbosity，通过解析后，其值保存在args.verbosity变量中.
  
        action参数表示值赋予键的方式，这里用到的是bool类型；如果是'count'表示将--verbose标签出现的次数作为verbose的值；
        'append'表示将每次出现的该便签后的值都存入同一个数组再赋值。这里action的意思是当读取的参数中出现--verbosity/-v的时候，
        参数字典的verbosity建对应的值为True，通过定义参数时指定action="store_true"，可以不需要在-v后面指定参数值。
        
        required 指定该参数是否必须的
        
        dest 指定参数名，不指定的话，默认情况下，对于可选参数选取最长的名称，中划线转换为下划线.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true", default=False)
    parser.add_argument("-i", "--ignore", help="can be ignored", required=False, dest='bar')
    args = parser.parse_args()
    if args.verbosity:
        print("verbosity turned on, verbosity: " + str(args.verbosity))
    if args.bar:
        print("bar: " + str(args.bar))

    '''
        默认的参数类型为str，如果要进行数学计算，需要对参数进行解析后进行类型转换，如果不能转换则需要报错，
        argparse 通过type指定参数类型，对参数值进行对应类型的解析，如果类型不符合，则直接报错。
    '''
    # parser = argparse.ArgumentParser()
    # parser.add_argument('x', type=int, help="the base")
    # args = parser.parse_args()
    # answer = args.x ** 2
    # print(answer)


    '''
        choices 可以限定参数值的输入范围
        default 指定参数默认值
    '''
    # parser = argparse.ArgumentParser()
    # parser.add_argument("square", type=int, help="display a square of a given number")
    # parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],  default=1, help="increase output verbosity")
    #
    # args = parser.parse_args()
    # answer = args.square ** 2
    #
    # if args.verbosity == 2:
    #     print("the square of {} equals {}".format(args.square, answer))
    # elif args.verbosity == 1:
    #     print("{}^2 == {}".format(args.square, answer))
    # else:
    #     print(answer)


    '''
        description 给整个程序定义帮助文档
        add_mutually_exclusive_group 定义互斥组参数，即所添加的参数，在同一条指令中，只能出现一个
    '''

    # parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument("-v", "--verbose", action="store_true")
    # group.add_argument("-q", "--quiet", action="store_true")
    # parser.add_argument("x", type=int, help="the base")
    # parser.add_argument("y", type=int, help="the exponent")
    # args = parser.parse_args()
    # answer = args.x ** args.y
    #
    # if args.quiet:
    #     print(answer)
    # elif args.verbose:
    #     print("{} to the power {} equals {}".format(args.x, args.y, answer))
    # else:
    #     print("{}^{} == {}".format(args.x, args.y, answer))