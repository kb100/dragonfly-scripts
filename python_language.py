from dragonfly import *


class PythonRule(MappingRule):
    mapping = {
        # Commands and keywords:
        "and": Text(" and "),
        "as": Text("as "),
        "assign": Text(" = "),
        "assert": Text("assert "),
        "break": Text("break"),
        "comment": Text("# "),
        "class": Text("class "),
        "continue": Text("continue"),
        "del": Text("del "),
        "divided by": Text(" / "),
        "(dict|dictionary) key value": Text("\"\": \"\",") + Key("left:6"),
        "enumerate": Text("enumerate()") + Key("left"),
        "(def|define|definition) [function]": Text("def "),
        "(def|define|definition) init": Text("def __init__("),
        "doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),
        "else": Text("else:") + Key("enter"),
        "except": Text("except "),
        "exec": Text("exec "),
        "(el if|else if)": Text("elif "),
        "equals": Text(" == "),
        "false": Text("False"),
        "finally": Text("finally:") + Key("enter"),
        "for": Text("for "),
        "from": Text("from "),
        "global ": Text("global "),
        "greater than": Text(" > "),
        "greater [than] equals": Text(" >= "),
        "if": Text("if "),
        "in": Text(" in "),
        "is": Text(" is "),
        "(int|I N T)": Text("int()") + Key("left"),
        "init": Text("init"),
        "import": Text("import "),
        "(len|L E N)": Text("len("),
        "lambda": Text("lambda "),
        "less than": Text(" < "),
        "less [than] equals": Text(" <= "),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "not": Text(" not "),
        "not equals": Text(" != "),
        "none": Text("None"),
        "or": Text(" or "),
        "pass": Text("pass"),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "print": Text("print()") + Key("left"),
        "raise": Text("raise"),
        "raise exception": Text("raise Exception()") + Key("left"),
        "return": Text("return "),
        "self": Text("self"),
        "(str|S T R)": Text("str"),
        "triple quote": Key("dquote,dquote,dquote"),
        "true": Text("True"),
        "try": Text("try:") + Key("enter"),
        "times": Text(" * "),
        "with": Text("with "),
        "while": Text("while "),
        "yield": Text("yield "),
        # Some common modules.
        "datetime": Text("datetime"),
        "(io|I O)": Text("io"),
        "logging": Text("logging"),
        "(os|O S)": Text("os"),
        "(pdb|P D B)": Text("pdb"),
        "(re|R E)": Text("re"),
        "(sys|S Y S)": Text("sys"),
        "S Q lite 3": Text("sqlite3"),
        "subprocess": Text("subprocess"),
    }
