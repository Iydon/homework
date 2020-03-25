# -*- encode: utf-8 -*-
from sympy import symbols, Sum, oo, pretty


n = symbols('n', integer=True)
a_0 = symbols('a_0')


def sum_progression(a_n, end):
    r'''\sum^{end}_{n=1} a_n
    '''
    expr = Sum(a_n, (n, 1, end))
    return expr.doit()


def sum_geometric_progression(end=oo):
    r'''\sum^{end}_{n=1} a_0 r^n
    '''
    r = symbols('r')
    a_n = a_0 * r**n
    return sum_progression(a_n, end)


def sum_arithmetric_progression(end=n):
    r'''\sum^{end}_{n=1} a_0 + nd
    '''
    d = symbols('d')
    a_n = a_0 + n*d
    return sum_progression(a_n, end)


def echo_expression_without_unicode(expr, echo=print):
    '''sympy.pretty_print
    '''
    result = pretty(expr,
        use_unicode=False,
        use_unicode_sqrt_char=False)
    echo(result)


if __name__ == '__main__':
    expr_gp = sum_geometric_progression()
    echo_expression_without_unicode(expr_gp)

    expr_ap = sum_arithmetric_progression()
    echo_expression_without_unicode(expr_ap)
