#!/usr/bin/env python
# -*- coding:utf-8 -*-

import arsparse


#使用argparse的第一步是创建一个ArgumentParser对象,ArgumentParser对象会保存把命令行解析成python数据类型所需要的所有信息
parser = arsparse.ArgumentParser()

#通过调用add_argument()方法向ArgumentParser添加程序的参数信息，通常情况下，
  #这些信息告诉ArgumentParser如何接收命令行上的字符串并将它们转换成对象， 这些信息被保存下来并在调用parse_args()时用到。 例如：
parse.add_argument('-H', '--host', help='host ip addr', type=str)
parse.add_argument('-P', '--port', help='host port', type=int)
parse.add_argument('-u', '--user', help='host user', type=str)
parse.add_argument('-c', '--cmd', help='command', type=str, nargs='+')


# 例子：
>>> parser.add_argument('integers', metavar='N', type=int, nargs='+',
...                     help='an integer for the accumulator')
>>> parser.add_argument('--sum', dest='accumulate', action='store_const',
...                     const=sum, default=max,
...                     help='sum the integers (default: find the max)')

#接下来，调用parse_args()返回的对象将带有两个属性，integers和accumulate， 属性integers将是一个包一个或多个整数的列表，
  #如果命令行上指定 --sum， 那么属性accumulate将是sum() 函数， 如果没有指定，则是max()函数

# 解析参数：
# ArgumentParser 通过 parse_args()方法解析参数，它将检查命令行把每个参数转换成恰当的类型并采取恰当的动作。
   #在大部分情况下，这意味着将从命令行中解析出来的属性建立一个简单的Namespace对象

>>> parser.parse_args(['--sum', '7', '-1', '42'])
Namespace(accumulate=<built-in function sum>, integers=[7, -1, 42]) 
#在脚本中，parse_args() 调用一般不带参数，ArgumentParser将根据sys.argv自动确定命令行参数

    args = parse.parse_args()
    if  args.host is None or \
        args.port is None or \
        args.user is None or \
        args.cmd is None:
        parse.print_help()
    else:
         pwd = getpass.getpass('请输入密码')
         ssh_connect(args.host, args.port, args.user, pwd, args.cmd)

#    logging.basicConfig(level=logging.INFO)
#    ssh_connect('192.168.10.87', 22, 'root', 'Hqsb@@##', ['id', 'ifconfig'])


# ArgumentParser 对象：
#class argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, 
	#prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True)¶

#创建一个新的ArgumentParser对象， 所有的参数应该以关键字参数传递，下面有对每个参数各自详细描述，但是剪短地讲它们是：
 * prog         -   程序的名字 (默认：sys.argv[0])
 * usage        -   描述程序用法的字符串(默认：从解析器的参数生成)
 * description  -   参数帮助信息之前的文本(默认： 空)
 * epilog       -   参数帮助信息之后的文本(默认：空)
 * parents - ArgumentParser 对象的一个列表，这些对象的参数应该包括进去
 * formatter_class - 定制化帮助信息的类
 * prefix_chars - 可选的参数的前缀字符集(默认： '_')
 * fromfile_prefix_chars - 额外的参数应该读取的文件的前缀字符集(默认：None)
 * argument_default - 参数的全局默认值(默认:None)
 * conflict_handler - 解决冲突的可选参数的策略(通常没有必要)
 * add_help - 给解析器添加-h/-help选项 (默认：True)


#prog 参数：
#默认情况下，ArgumentParser对象使用sys.argv[0] 决定在帮助信息中，如何显示程序的名字，这个默认值几乎总能满足需求，
   #因为帮助信息(中的程序名称) 会自动匹配命令行中调用的程序名称，例如，参考下面这段myprogram.py文件中的代码

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', help='foo help')
args = parser.parse_args()

该程序的帮助信息将显示myprogram.py作为程序的名字(无论程序是在哪里被调用的);
$ python myprogram.py --help
usage: myprogram.py [-h] [--foo FOO]

optional arguments:
-h, --help  show this help message and exit
--foo FOO   foo help
$ cd ..
$ python subdir\myprogram.py --help
usage: myprogram.py [-h] [--foo FOO]

optional arguments:
 -h, --help  show this help message and exit
 --foo FOO   foo help

# 如果要改变这个默认的行为， 可以使用prog=参数给ArgumentParser提供另外一个值
>>> parser = argparse.ArgumentParser(prog='myprogram')
>>> parser.print_help()
usage: myprogram [-h]

optional arguments:
 -h, --help  show this help message and exit

# 注意，无论是来自sys.argv[0]还是来自prog=argument, 在帮助信息中都可以使用%(prog)s格式符得到程序的名字
>>> parser = argparse.ArgumentParser(prog='myprogram')
>>> parser.add_argument('--foo', help='foo of the %(prog)s program')
>>> parser.print_help()
usage: myprogram [-h] [--foo FOO]

optional arguments:
 -h, --help  show this help message and exit
 --foo FOO   foo of the myprogram program


#usage 参数：
# 默认情况下，ArgumentParser依据它包含的参数计算出帮助信息；
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('--foo', nargs='?', help='foo help')
>>> parser.add_argument('bar', nargs='+', help='bar help')
>>> parser.print_help()
usage: PROG [-h] [--foo [FOO]] bar [bar ...]

positional arguments:
 bar          bar help

optional arguments:
 -h, --help   show this help message and exit
 --foo [FOO]  foo help

# 可以通过关键字参数usage=覆盖默认的信息：
>>> parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
>>> parser.add_argument('--foo', nargs='?', help='foo help')
>>> parser.add_argument('bar', nargs='+', help='bar help')
>>> parser.print_help()
usage: PROG [options]

positional arguments:
 bar          bar help

optional arguments:
 -h, --help   show this help message and exit
 --foo [FOO]  foo help

 在你的帮助信息中，可以使用%(prog)s 格式指示符替代程序的名字
  操作系统的进程空间可分为用户空间和内核空间，它们需要不同的执行权限。其中系统调用运行在内核空间。 

ArgumentParser构造器的大部分调用都将使用description=关键字参数， 这个参数给出程序做什么以及如何工作的简短描述，
	在帮助信息中，该描述在命令行用法字符串和各个参数的帮助信息之间显示：

>>> parser = argparse.ArgumentParser(description='A foo that bars')
>>> parser.print_help()
usage: argparse.py [-h]

A foo that bars

optional arguments:
 -h, --help  show this help message and exit

默认情况下， 该描述会换行以适应给定的空间。 如果要改变这个默认的行为，可以参考formatter_class参数


## epilog 参数：
有些程序喜欢在参数的描述之后显示额外的关于程序的描述，这些文本可以使用ArgumentParser的epilog=参数指定：
>>> parser = argparse.ArgumentParser(
...     description='A foo that bars',
...     epilog="And that's how you'd foo a bar")
>>> parser.print_help()
usage: argparse.py [-h]

A foo that bars

optional arguments:
 -h, --help  show this help message and exit

And that's how you'd foo a bar
和description一样，epilog=文本默认会换行，但是可以通过ArgumentParser的formatter_class参数调整这个行为。


## parents 参数
有时候， 几个解析器会共享一个共同的参数集，可以使用一个带有所有共享参数的解析器传递给ArgumentParser的
	parents=参数，而不用重复定义这些参数，parents=参数接受一个ArgumentParser对象的列表
	然后收集它们当中所有的位置参数和可选参数，并将这些参数添加到正在构建的ArgumentParser对象：

>>> parent_parser = argparse.ArgumentParser(add_help=False)
>>> parent_parser.add_argument('--parent', type=int)

>>> foo_parser = argparse.ArgumentParser(parents=[parent_parser])
>>> foo_parser.add_argument('foo')
>>> foo_parser.parse_args(['--parent', '2', 'XXX'])
Namespace(foo='XXX', parent=2)

>>> bar_parser = argparse.ArgumentParser(parents=[parent_parser])
>>> bar_parser.add_argument('--bar')
>>> bar_parser.parse_args(['--bar', 'YYY'])
Namespace(bar='YYY', parent=None)
注意大部分父解析器将指定add_help=False , 否则,ArgumentParser将看到两个-h/--help 选项(一个在父解析器，一个在子解析器中)
	并引发错误。

注意： 在通过parents=传递父解析器之前，你必须完全初始化它们，如果在子解析器之后你改变了父解析器， 这些改变不会反映在子解析器中



formatter_class参数
ArgumentParser对象允许通过指定一个格式化类来定制帮助信息的格式，当前，有三个种这样的类：
class argparse.RawDescriptionHelpFormatter
class argparse.RawTextHelpFormatter
class argparse.ArgumentDefaultsHelpFormatter	

前两个在文本信息如何显示上允许更多控制，最后一个会自动添加关于参数默认值的信息
默认情况下，ArgumentParser对象会对命令行帮助信息中的description和epilog文本进行换行：
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     description='''this description
...         was indented weird
...             but that is okay''',
...     epilog='''
...             likewise for this epilog whose whitespace will
...         be cleaned up and whose words will be wrapped
...         across a couple lines''')
>>> parser.print_help()
usage: PROG [-h]

this description was indented weird but that is okay

optional arguments:
 -h, --help  show this help message and exit

likewise for this epilog whose whitespace will be cleaned up and whose words
will be wrapped across a couple lines

把RawDescriptionHelpFormatter传递给formatter_class=表示description和epilog已经是正确的格式而不应该在折行：
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.RawDescriptionHelpFormatter,
...     description=textwrap.dedent('''\
...         Please do not mess up this text!
...         --------------------------------
...             I have indented it
...             exactly the way
...             I want it
...         '''))
>>> parser.print_help()
usage: PROG [-h]

Please do not mess up this text!
--------------------------------
   I have indented it
   exactly the way
   I want it

optional arguments:
 -h, --help  show this help message and exit

RawDescriptionHelpFormatter将保留所有帮助的文本的空白，包括参数的描述。
另外一个格式化类ArgumentDefaultsHelpFormatter，将添加每个参数的默认值信息
>>> parser = argparse.ArgumentParser(
...     prog='PROG',
...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
>>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
>>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
>>> parser.print_help()
usage: PROG [-h] [--foo FOO] [bar [bar ...]]

positional arguments:
 bar         BAR! (default: [1, 2, 3])

optional arguments:
 -h, --help  show this help message and exit
 --foo FOO   FOO! (default: 42)


 # prefix_chars参数：
 大部分命令行选项使用-作为前缀， 例如-f/-foo 需要指出不同的或者额外的前缀字符的解析器，例如类似+f或者/foo这样的选项，
 	可以使用ArgumentParser构造器的prefix_chars=参数指定它们：
>>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
>>> parser.add_argument('+f')
>>> parser.add_argument('++bar')
>>> parser.parse_args('+f X ++bar Y'.split())
Namespace(bar='Y', f='X')

prefix_chars=参数默认为'_', 提供不包含-的字符集将导致不允许-f/--foo选项。


#fromfile_prefix_chars参数
有时候，例如处理一个特别长的参数列表的时候，把参数列表保存在文件中而不是在命令行中敲出来可能比较合理，
	如果给出ArgumentParser构造器的fromfile_prefix_chars=参数，那么以任意一个给定字符开始的参数将被
	当做文件，并且将被这些文件包含的参数替换。例如：

>>> with open('args.txt', 'w') as fp:
...    fp.write('-f\nbar')
>>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
>>> parser.add_argument('-f')
>>> parser.parse_args(['-f', 'foo', '@args.txt'])
Namespace(f='bar')
从文件中读入的参数必须默认是每行一个参数，(但另可参阅convert_arg_line_to_args()) 并且将被当做在命令行
上原始文件所在的位置，所有在上面的例子中，表达式['-f', 'foo', '@args.txt']被认为等同于表达式['-f', 'foo', '-f', 'bar']
fromfile_prefix_chars=参数默认为None, 意味着参数永远不会被当做文件


argument_default参数：
通常情况下，参数默认值的指定通过传递一个默认值add_argument()或者以一个指键-值对的集合调用set_defaults()方法
	然而又时候，指定一个解析器范围的参数默认值会比较有用，这可以通过传递argument_default=关键字参数给
	ArgumentParser完成。例如，为了全局地阻止parse_args()调用时不必要的属性创建，我们可以提供argument_default=SUPPRESS

>>> parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
>>> parser.add_argument('--foo')
>>> parser.add_argument('bar', nargs='?')
>>> parser.parse_args(['--foo', '1', 'BAR'])
Namespace(bar='BAR', foo='1')
>>> parser.parse_args([])
Namespace()


# conflict_handler 参数
ArgumentParser对象不允许同一个选项具有两个动作，默认情况下，如果试图创建一个已经使用的选项,ArgumentParser对象将抛出异常。
>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo', help='old foo help')
>>> parser.add_argument('--foo', help='new foo help')
Traceback (most recent call last):
 ..
ArgumentError: argument --foo: conflicting option string(s): --foo
有时候（例如使用parents的时候）简单地用相同的选项覆盖旧的参数是有用的。为了得到这样的行为，可以提供'resolve'值给ArgumentParser的conflict_handler=参数： 	
>>> parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
>>> parser.add_argument('-f', '--foo', help='old foo help')
>>> parser.add_argument('--foo', help='new foo help')
>>> parser.print_help()
usage: PROG [-h] [-f FOO] [--foo FOO]

optional arguments:
 -h, --help  show this help message and exit
 -f FOO      old foo help
 --foo FOO   new foo help


 # add_argument()方法：
 ArgumentParser.add_argument(name or flags...[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])
定义应该如何解析一个命令行参数。下面每个参数有它们自己详细的描述，简单地讲它们是：

name or flags - 选项字符串的名字或者列表，例如foo 或者-f, --foo。
action - 在命令行遇到该参数时采取的基本动作类型。
nargs - 应该读取的命令行参数数目。
const - 某些action和nargs选项要求的常数值。
default - 如果命令行中没有出现该参数时的默认值。
type - 命令行参数应该被转换成的类型。
choices - 参数可允许的值的一个容器。
required - 该命令行选项是否可以省略（只针对可选参数）。
help - 参数的简短描述。
metavar - 参数在帮助信息中的名字。
dest - 给parse_args()返回的对象要添加的属性名称。


# name 或 flags 参数
add_argument()方法必须知道期望的是可选参数，比如-f或者--foo,还是位置参数， 比如一个文件列表，传递给add_argument()
	第一个参数因此必须是一个标记列或者意见简单的参数名字，例如，一个可选的参数可以像这样的创建
>>> parser.add_argument('-f', '--foo')

而一个位置参数可以像这样创建：
>>> parser.add_argument('bar')
当调用parse_args()时， 可选参数将以-前缀标识，剩余的参数将被假定为位置参数

>>> parser = argparse.ArgumentParser(prog='PROG')
>>> parser.add_argument('-f', '--foo')
>>> parser.add_argument('bar')
>>> parser.parse_args(['BAR'])
Namespace(bar='BAR', foo=None)
>>> parser.parse_args(['BAR', '--foo', 'FOO'])
Namespace(bar='BAR', foo='FOO')
>>> parser.parse_args(['--foo', 'FOO'])
usage: PROG [-h] [-f FOO] bar
PROG: error: too few arguments

#'+'。和'*'一样，出现的所有命令行参数都被收集到一个列表中。除此之外，如果没有至少出现一个命令行参数将会产生一个错误信息。例如：
#如果没有提供nargs关键字参数，读取的参数个数取决于action，通常这意味着读取一个命令行参数并产生一个元素(不是一个列表)

#1，Flask-RESTful插件介绍及应用
* Flask-RESTful 介绍：
* Flask-RESTful 请求解析：
* Flask-RESTful 的响应域:
* 重构程序:


1,包含以下几个知识点：
* Flask-RESTful概述
	Flask-RESTful是为了快速构建REST API的Flask插件， 它是能喝现有
	的ORM配合的轻量级数据抽象，Flask-RESTful鼓励小型化时间
		如果你熟悉Flask, Flask-RESTful将会非常简单易学。
		http://flask-restful.readthedocs.org/en/latest/index.html

* 实例
* 资源路由
* 参数解析
* 数据格式化

头像










