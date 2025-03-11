import re
from lark import Lark, Transformer, v_args
from tabulate import tabulate

gramatica = r'''
start: (PAR_COM_PARENTESIS|pt_tt_line|pt_line|tt_line|FIG_LINE|UNKNOWN_LINE)*

pt_tt_line: pt_line tt_line

pt_line: PT_LINE UNKNOWN_LINE*
tt_line: TETUN_LINE UNKNOWN_LINE*

PAR_COM_PARENTESIS.2: /(\b\w+\b )+\(.+\)/

PT_LINE.3: /PORTUGUÊS: .*/
TETUN_LINE.3: /TETUN: .*/

FIG_LINE.3: /Figura \d+\- (\b\w+\b )+\(.+\)/

UNKNOWN_LINE.1: /.+/

%import common.NEWLINE
%ignore NEWLINE
'''

ex = r'''
Simplificação de Radicais (Simplifikasaun hosi Radikál sira).................................................. 118
Sinais (Sinál Sira) ...................................................................................................................... 119
Sistema (Sistema) ...................................................................................................................... 119
Subtração (Subtrasaun / Hasai / Kuran) .................................................................................... 119
Subtraendo (Subtraendu / Hamenus)......................................................................................... 119
Tangente (Tanjente) .................................................................................................................. 120
Tangram (Tangram) .................................................................................................................. 120
Teorema (Teorema) ................................................................................................................... 121
Termo (Termu) .......................................................................................................................... 121
Tetraedro (Tetraedru) ................................................................................................................ 121
Trapézio (Trapéziu) ................................................................................................................... 121
Triângulo (Triángulu)................................................................................................................ 122
Trigonometria (Trigonometria) ................................................................................................. 122
Unidade (Unidade) .................................................................................................................... 122
Valor Absoluto (Valór Absolutu) .............................................................................................. 122
Valor Médio (Valór Médiu) ...................................................................................................... 122
Variável (Variavel).................................................................................................................... 122


PORTUGUÊS: Localização de um ponto em relação ao eixo horizontal x. Pode ter
posição positiva, negativa ou nula. Exemplos: Ver em TETUN.
TETUN: Fatin ba pontu sira-ne´ebé iha relasaun ho eixu orizontál (eixu x). Bele iha
pozisaun pozitiva, negativa ka nula. Ezemplu sira:

Figura 1- Eixo X-Y com abscissas (Eixu X-Y ho absisa)
'''

processador = Lark(gramatica, parser='lalr')
tree = processador.parse(ex)

print(tree.pretty())


@v_args(inline=True)
class T(Transformer):
    def start(self, *t): return t

    def PAR_COM_PARENTESIS(self, t): return ('pt-tt', re.split(r' *[()]', t.value)[:-1])

    def PT_LINE(self, t): return ('pt', t.value.split(':')[1])

    def pt_line(self, pt, *l): return ('pt', pt[1] + '\n' + '\n'.join(l))

    def TETUN_LINE(self, t): return ('tt', t.value.split(':')[1])

    def tt_line(self, tt, *l): return ('tt', tt[1] + '\n' + '\n'.join(l))

    def pt_tt_line(self, pt, tt): return ('pt-tt', [pt[1], tt[1]])

    def FIG_LINE(self, t): return ('fig', t.value)

    def UNKNOWN_LINE(self, t): return t.value


arvore = T().transform(tree)

unknown = list(filter(lambda x: type(x) == str, arvore))
print('UNKNOWN')
print(unknown)

arvore = filter(lambda x: type(x) != str, arvore)
arvore = list(map(lambda x: x[1], arvore))

print('DATA')
print(tabulate(arvore))
