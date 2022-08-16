import functools
import inspect
from operator import index
import re
import types
from typing import List

from expression import Expression

ONE_LINE_LAMBDA_PATTERN1 = re.compile(r"\(lambda (?P<params>.*): (?P<code>.*)\)\(.*\)")
ONE_LINE_LAMBDA_PATTERN2 = re.compile(r"lambda (?P<params>.*): (?P<code>.*)")

def _is_lambda(func) -> bool:
    return isinstance(func, types.LambdaType) and func.__name__ == "<lambda>"


def _extract_code_from_func(func, source: str) -> List[str]:
    # the way to parse should be more robust
    # parse params & code
    if _is_lambda(func):
        # extract lambda body from one line code
        if source.find("expression") != -1:
            expression_index = source.index("expression")
            before_expression = source[:expression_index]
            left_parentheses_cnt = before_expression.count("(")
            i = len(source) - 1
            while left_parentheses_cnt > 0:
                if source[i] == ")":
                    left_parentheses_cnt -= 1
                    break
                i -= 1
            lambda_source = source[expression_index + len("expression"):i]
        else:
            lambda_source = source.strip()
        # parse params and code
        m = ONE_LINE_LAMBDA_PATTERN1.match(lambda_source)
        if m is None:
            m = ONE_LINE_LAMBDA_PATTERN2.match(lambda_source)
        params = m.group("params")
        code = "return " + m.group("code")  # manually add return for lambda
    else:
        lines = lines[1:]  # remove @expression line
        lines = source.split("\n")
        return [line.lstrip("    ") for line in lines[2:] if line]
    # normalize names
    params = params.replace(" ", "").split(",")  # str => list of param names
    normalized_names = []
    param_index = 0
    for param in params:
        input_name = f"input_{param_index}"
        normalized_names.append(input_name)
        param_index += 1
        code = code.replace(param, input_name)
    return normalized_names, code
    

def expression(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            source = inspect.getsource(func)
        except TypeError:
            source = func.__name__
        normalized_names, code = _extract_code_from_func(func, source)
        return Expression(normalized_names, code, *args, **kwargs)
    return wrapper
