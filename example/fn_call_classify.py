"""
Use OpenAI's new function calling API to define the possible outputs 
and then use the "input" argument it returns as the classification

link: https://twitter.com/_ScottCondron/status/1670827747684364288

问：
这个情感分类没有prompt，到底是怎么做到的？里面定义的这个函数print_sentiment也没有具体的定义呀？

答：
1. 因为function_call指定了要执行print_sentiment函数; 
2. 所以会看函数描述和参数，这两实际构成了Prompt，尤其是参数的enum

https://promptknit.com 可以类似playground 测试 function
"""

import openai
import sys
import json


def classify(input_string:str) ->str:
    functions = [{
        "name" : "print_sentiment",
        "description": "A function that prints the given sent iment", 
        "parameters": {
            "type" : "object",
            "properties": {
                "sentiment":{
                    "type": "string",
                    "enum" : ["positive", "negative", "neutral"], 
                    "description": "The sentiment."
                }
            },
        "required": ["sentiment"]
        }
    }]

    messages = [{"role": "user", "content" : input_string}] 
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call={"name":"print_sentiment"} # function_call指定了要执行print_sentiment函数
    )

    function_call = response.choices[0].message["function_call"] 
    argument = json.loads(function_call["arguments"]) 
    return argument


if __name__ =='__main__':
    print(classify(sys.argv[1]))
