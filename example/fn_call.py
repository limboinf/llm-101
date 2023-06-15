'''
OpenAI Function Calling Model.

重点：
- function_call ：模型决定调用一个函数
- 根据语义匹配

usage:
python example/fn_call.py 当前位置：Beijing,Chain, 现在天气怎么样？ 0
python example/fn_call.py 可以赞助我2块钱买包辣条吗？ 0

python example/fn_call.py 我和马云谁能买得起北京的房子 0
python example/fn_call.py 我和马云谁最帅 0

refs:
- https://platform.openai.com/docs/guides/gpt/function-calling
- https://gist.github.com/xtekky/28e1320d593e04e586ba2da807778176
- https://twitter.com/ProgramerJohann/status/1668812508608724994?s=20 提供了流程图挺好的

'''
import random
import sys
import json
import requests
import openai
from datetime import datetime
import inspect
from typing import get_type_hints

from app.init import init_llm
init_llm()


def to_json(func) -> str:
    '''
    Function to convert a Python function to JSON representation
    Pass to the Chat API model 'gpt-3.5-turbo-0613' or 'gpt-4-0613' as a function
    
    eg:
    {
        'name': 'get_current_weather',
        'description': 'get weather in location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {'description': 'CityName, CountryCode', 'type': 'string'}
            }
        }
    }
    '''
    json_representation = dict()
    json_representation['name'] = func.__name__
    json_representation['description'] = func.__doc__.strip()

    # Get function parameters and their type hints
    parameters = inspect.signature(func).parameters
    func_type_hints = get_type_hints(func)

    json_parameters = dict()
    json_parameters['type'] = 'object'
    json_parameters['properties'] = {}

    # Process each parameter
    for name, param in parameters.items():
        if name == 'return':
            continue

        param_info = {}

        # Parameter description from the default value
        param_info['description'] = inspect.signature(func).parameters[name].default

        param_annotation = func_type_hints.get(name)

        if param_annotation:
            # Convert parameter type hint to JSON type
            if param_annotation.__name__ == 'str':
                param_info['type'] = 'string'
            else:
                param_info['type'] = param_annotation.__name__

        if name == 'self':
            continue

        json_parameters['properties'][name] = param_info

    json_representation['parameters'] = json_parameters

    return json_representation


def format_call(function_call: dict) -> str:
    '''
    将函数调用格式化为字符串的函数
    
    eg:
    {
        "id": "chatcmpl-xxx",
        "object": "chat.completion",
        "created": 1686729988,
        "model": "gpt-3.5-turbo-0613",
        "choices": [
            {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": null,
                "function_call": {
                "name": "get_current_weather",
                "arguments": "{\n  \"location\": \"New York, USA\"\n}"
                }
            },
            "finish_reason": "function_call"
            }
        ],
        "usage": {
            "prompt_tokens": 103,
            "completion_tokens": 19,
            "total_tokens": 122
        }
    }
    
    转换为 get_current_weather()
    '''
    json_data: dict = json.loads(function_call.__str__())

    function_name: str = json_data["name"]
    args_json: str = json_data["arguments"]
    args_dict: dict = json.loads(args_json)
    args: str = ', '.join([f"{k}='{v}'" for k, v in args_dict.items()])

    return f"{function_name}({args})"


def get_current_weather(location: str = 'CityName, CountryCode'):
    """获取城市天气情况
    
    location: 格式 CityName, CountryCode, 如 Beijing, China
    """

    weather_data = requests.get(f'https://openweathermap.org/data/2.5/weather?q={location}&appid=439d4b804bc8187953eb36d2a8c26a02').json()

    print(f'\nAPI Request: {location} ...\n')

    return json.dumps(
        separators=(',', ':'),
        obj={
            'description': weather_data['weather'][0]['description'],
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity']
            }
        )


def get_your_money(account: str = ''):
    """把你的钱给我

    Args:
        account (str): 账号名
    """
    print(f'\n把钱给我: {account} ...\n')
    return json.dumps({'account': account, 'money': int(random.random()*1000)})


weather_function_json = to_json(get_current_weather)
money_function_json = to_json(get_your_money)


# ----------------------------------------------------------------
# ask_weather bot
# ----------------------------------------------------------------


def ask_weather(question: str, debug: bool = False):
    """weather bot

    Args:
        location (str, optional): 如Beijing,China.
    """

    prompt = [
        {
            'role': 'assistant',
            'content': f'你是一个天气预报助手回答指定日期 date: {datetime.today().strftime("%Y/%m/%d %H:%M:%S")} 天气。'
        },
        {
            'role': 'user',
            'content': '{question}'
        }
    ]

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=prompt,
        functions=[weather_function_json]
    )

    if debug:
        # 从返回的参数可以看出如果匹配到你设定的内容, 会响应多一个属性的内容，就是function_call。
        # 里面包含你前面设定的函数名 get_current_weather 和匹配到的参数数组arguments。
        print(f'01 ----------\n {completion} \n----------')

    if 'function_call' in completion.choices[0].message:
        # 把上面返回的funciton_call函数本地调用下，把结果添加到下轮对话中
        # 也可以直接让funciton_call函数本地调用的结果直接输出，不再经过一轮GPT对话。
        # 一般会将响应结果发送给OpenAI进行总结，然后再返回给用户。
        prompt.append(
            {
                'role': 'function',         # function role
                'name': completion.choices[0].message.function_call.name,
                'content': eval(format_call(completion.choices[0].message.function_call))
            }
        )

        if debug:
            print(f'02 ----------\n {prompt} \n----------')

        # 使用更新的函数调用继续对话。
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=prompt,
            functions=[weather_function_json]
        )
        
        if debug:
            print(f'03 ----------\n {completion} \n----------')

        # Print the generated response
        print(completion.choices[0].message.content)
    else:
        print(f'没有找到functin_call, 直接回答 ===> \n{completion.choices[0].message.content}')


# ----------------------------------------------------------------
# ask_weather bot
# ----------------------------------------------------------------

def ask_your_money(question: str, debug: bool = False):
    system_prompt = {
        'role': 'assistant',
        'content': '你是借贷平台，当涉及到有金钱时，回答我金额'
    }
    
    # 相关的问题, response里会有 function_call
    # 不相关的问题, response里不会有 function_call
    user_prompt = {'role': 'user', 'content': question}
    prompt = [system_prompt, user_prompt]

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=prompt,
        functions=[weather_function_json, money_function_json]
    )

    if debug:
        print(f'01 ----------\n {completion} \n----------')

    if 'function_call' in completion.choices[0].message:
        print(f'Response 存在 function_call: {completion.choices[0].message.function_call.name}')
        prompt.append(
            {
                'role': 'function',         # function role
                'name': completion.choices[0].message.function_call.name,
                'content': eval(format_call(completion.choices[0].message.function_call))
            }
        )

        if debug:
            print(f'02 ----------\n {prompt} \n----------')

        # 使用更新的函数调用继续对话。
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=prompt,
            functions=[weather_function_json, money_function_json]
        )
        
        if debug:
            print(f'03 ----------\n {completion} \n----------')

        # Print the generated response
        print(completion.choices[0].message.content)
    else:
        print(f'没有找到functin_call, 直接回答 ===> \n{completion.choices[0].message.content}')


if __name__ == '__main__':
    q = sys.argv[1]
    debug = sys.argv[2]
    debug = True if debug.lower() in ['true', '1'] else False 
    
    # ask_your_money(q, debug=debug)
    ask_weather(q, debug=debug)