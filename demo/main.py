"""Omit import of azure-ai-ml and mldesigner."""
from expression_decorator import expression


@expression
def max_func(input1, input2, input3):
    return max(input1, input2, input3)


def compare_silo_output_func(silo_output_delta: int):
    silo_output_delta.export()  # this can be regarded as convert to command component


def pipeline_with_expression(
    silo1_output1: int, silo1_output2: int, silo1_output3: int,
    silo2_output1: int, silo2_output2: int, silo2_output3: int,
):
    # # TODO: only consider lambda scenario for now
    # silo1_output_max = max_func(silo1_output1, silo1_output2, silo1_output3)
    # silo2_output_max = max_func(silo2_output1, silo2_output2, silo2_output3)

    # one line lambda 1
    silo1_max = expression(lambda _input1, _input2, _input3: max(_input1, _input2, _input3))(silo1_output1, silo1_output2, silo1_output3)
    # one line lambda 2
    silo2_max = expression(
        lambda _input1, _input2, _input3: max(_input1, _input2, _input3)
    )(silo2_output1, silo2_output2, silo2_output3)
    
    # # TODO: multi line lambda
    # lambda_func = lambda _input1, _input2, _input3: \
    #     min(_input1, _input2, _input3)
    # silo1_min = expression(lambda_func)(silo1_output1, silo1_output2, silo1_output3)
    
    # # TODO: suffix comment
    # silo2_min = expression(lambda _input1, _input2, _input3: min(_input1, _input2, _input3))(silo2_output1, silo2_output2, silo2_output3)  # one line lambda 3
    
    silo1_min = expression(lambda _input1, _input2, _input3: min(_input1, _input2, _input3))(silo1_output1, silo1_output2, silo1_output3)
    silo2_min = expression(lambda _input1, _input2, _input3: min(_input1, _input2, _input3))(silo2_output1, silo2_output2, silo2_output3)    
    
    silo_output_delta=expression(
        lambda _silo1_max, _silo1_min, _silo2_max, _silo2_min: (_silo1_max + _silo2_max) - (_silo1_min + _silo2_min)
    )(silo1_max, silo1_min, silo2_max, silo2_min)
    compare = compare_silo_output_func(silo_output_delta=silo_output_delta)


if __name__ == "__main__":
    pipeline = pipeline_with_expression(
        silo1_output1=1, silo1_output2=2, silo1_output3=3,
        silo2_output1=4, silo2_output2=5, silo2_output3=6,
    )

# output
"""
['input_1', 'input_2', 'input_3', 'input_6', 'input_7', 'input_8']
input_0 = max(input_1, input_2, input_3)
input_4 = min(input_1, input_2, input_3)
input_5 = max(input_6, input_7, input_8)
input_9 = min(input_6, input_7, input_8)
return (input_0 + input_5) - (input_4 + input_9)
"""
