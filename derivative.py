def central_difference_derivative(function, dx, **kwargs):
    h = 0.00001

    input_forward = kwargs.copy()
    input_backward = kwargs.copy()

    for param in [x for x in kwargs if x not in function.__code__.co_varnames]:
        del input_forward[param]
        del input_backward[param]

    if dx in input_forward:
        input_forward[dx] += h
        input_backward[dx] -= h

    return (function(**input_forward) - function(**input_backward)) / (2 * h)
