# Expression decorator demo

Demo for `@expression`, target to verify whether it is doable.

**For demo output**, refer to /demo/main.py, scroll down and you can see comment at the bottom.

Currently implement an init version, which:

- convert expression into object which records statments, and it can be merged
- (limitation) only support one line lambda function
- (need to refine) naive parse method for function code (may need AST library to do that in robust way)

Follow ups & thoughts:

- support multi-line lambda function and def function. Because we need to parse the arguments and function body, we may ask customer to write function in very strict (or say standard) style, below list two examples:

```python
# parameters in one line
def f(x, y):
    ...


# parameters in multi-line
def f2(
    x: int,
    y: int,
):
    ...

# typing should be optional

```
