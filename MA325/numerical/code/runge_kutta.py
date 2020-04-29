import sympy


def runge_kutta(f, t, y, h, m=4):
    '''Runge-Kutta method

    Examples:
        >>> ...
    '''
    # parameters
    𝜆s = sympy.symbols(f'𝜆1:{m+1}')
    𝛼s = sympy.symbols(f'𝛼2:{m+1}')
    𝛽s = [sympy.symbols(f'𝛽{i+2}(1:{i+2})') for i in range(m-1)]
    # Ks
    Ks = [None] * m
    Ks[0] = h * f(t, y)
    for i in range(m-1):
        t_ = t + 𝛼s[i]*h
        y_ = y + sum(𝛽*K for 𝛽, K in zip(𝛽s[i], Ks[:i+1]))
        result, _ = taylor_in_two_variables(f, t_, y_, t, y, m-1, error=False)
        Ks[i+1] = h * result
    # y_{n+1} - y_{n}
    Y = f(t, y)
    T = h * Y
    I = sympy.integrate(f(t, y), t)
    for i in range(m-1):
        Y = sympy.diff(Y.subs(y, I), t).subs(I, y)
        T += h**(i+2)/sympy.factorial(i+2) * Y
    T = T.subs(I, y)
    # combine parameters
    R = sum(𝜆*K for 𝜆, K in zip(𝜆s, Ks))
    T = (T-R).simplify()
    x = sympy.symbols('x')
    i = 1
    for j in range(m-1, -1, -1):
        for k in range(j+1):
            T = T.subs(sympy.diff(f(t, y), (t, k), (y, j-k)), x**i)
    coeffs = sympy.polys.poly(T, x).all_coeffs()
    sympy.pretty_print(tuple(filter(bool, coeffs)))
    return R


def taylor_in_two_variables(f, t, y, t0, y0, order, error=True):
    '''
    Example:
        >>> import sympy
        >>> t, y, t0, y0 = sympy.symbols('t, y, t0, y0')
        >>> f = sympy.Function('f')
        >>> print(taylor_in_two_variables(f, t, y, t0, y0, order=2))
    '''
    def nchoosek(n, k):
        g = sympy.factorial
        return g(n) / (g(k)*g(n-k))

    g = lambda n, i: (t-t0)**(n+1-i)*(y-y0)**i * nchoosek(n+1, i)
    h = lambda n, i, t=t0, y=y0: sympy.diff(f(t, y), (t, n+1-i), (y, i))
    result = f(t0, y0) + sum(
        sum(g(n, i)*h(n, i) for i in range(n+2)) / sympy.factorial(n+1)
        for n in range(order)
    )
    if error:
        ξ, µ = sympy.symbols('ξ, µ')
        error = sum(
            g(order, i)*h(order, i, ξ, µ) for i in range(order+2)
        ) / sympy.factorial(order+1)
    else:
        error = None
    return result, error


if __name__ == '__main__':
    t, y, t0, y0, h = sympy.symbols('t, y, t0, y0, h')
    f = sympy.Function('f')
    order = 2
    # result, error = taylor_in_two_variables(f, t, y, t0, y0, order, error=True)
    # sympy.pretty_print(result)
    # sympy.pretty_print(error)

    m = 2
    result = runge_kutta(f, t, y, h, m)
    sympy.pretty_print(result)
