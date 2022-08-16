import inspect

one_line_lambda = lambda x: x ** 2
multi_line_lambda1 = \
    lambda x: x ** 2
multi_line_lambda2 = \
    lambda x: \
    x ** 2

print(inspect.getsource(one_line_lambda))  # need to remove prefix & suffix
print(inspect.getsource(multi_line_lambda1))  # ideal input
print(inspect.getsource(multi_line_lambda2))  # need to deal with multiple lines
print(inspect.getsource(
    lambda x:
    x ** 2
))  # will miss something, may need to log to confirm

# output
"""
one_line_lambda = lambda x: x ** 2

    lambda x: x ** 2

    lambda x: \
    x ** 2

    lambda x:

"""
