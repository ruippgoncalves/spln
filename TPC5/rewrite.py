from lark import Lark, Transformer

dsl_grammar = r"""
start: function+

function: "defr" IDENTIFIER ":" NEWLINE rule+

rule: (substitution_rule | lambda_rule) NEWLINE

substitution_rule: BASE _ARROW IDENTIFIER
lambda_rule: BASE _ARROW_EVAL /[^\n]+/

BASE: IDENTIFIER | /[^ ]+/

IDENTIFIER.1: /[a-zA-Z_][a-zA-Z_0-9]*/
_ARROW.2: "==>"
_ARROW_EVAL.2: "=e=>"

%import common.NEWLINE
%import common.WS
%ignore WS
"""

class DSLTransformer(Transformer):
    def start(self, items):
        code = ""
        for func in items:
            code += func
        return code

    def function(self, items):
        func_name, _, *rules = items
        code = f"def transform_{func_name}(t):\n"
        for rule in rules:
            code += f"    {rule}\n"
        code += "    return t\n"
        return code

    def rule(self, items):
        rule, _ = items
        return rule

    def substitution_rule(self, items):
        old_word, new_word = items
        return f"t = re.sub(r'\\b{old_word}\\b', '{new_word}', t)"

    def lambda_rule(self, items):
        regex, transformer = items
        return f"t = re.sub(r'\\b{regex}\\b', {transformer}, t)"

dsl_parser = Lark(dsl_grammar, parser='lalr', transformer=DSLTransformer())

dsl_code = """
defr a:
    the ==> o
    cat ==> gato

defr b:
    chicken ==> galinha
    (\\w+) =e=> lambda x: dicionario.get(x[1], x[1])
"""

python_code = dsl_parser.parse(dsl_code)
print(python_code)
