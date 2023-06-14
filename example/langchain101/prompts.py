"""
Prompt
==================
docs: 
- https://python.langchain.com/en/latest/modules/prompts/prompt_templates/getting_started.html
"""

from langchain import PromptTemplate, FewShotPromptTemplate


# simple way, take any number of input variables.
template = 'xxx {product}'
prompt = PromptTemplate(template=template, input_variables=['product'])
s = prompt.format(product='apple')
print(s)

# or from_template to build
p2 = PromptTemplate.from_template(template)
print(p2.input_variables)
print(p2.format(product='sony'))

# FewShotPromptTemplate
# First, create the list of few shot examples.
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]

example_formatter_template = """Word: {word}
Antonym: {antonym}
"""

example_prompt = PromptTemplate(
    input_variables=['word', 'antonym'],
    template=example_formatter_template
)

# 为了生成带有少量样例的提示，您可以使用FewShotPromptTemplate。
# 这个类接受一个PromptTemplate和一个少量样例的列表。然后，它使用这些少量样例格式化提示模板。
# create FewShotPromptTemplate object
few_shot_prompt = FewShotPromptTemplate(
    # There are the examples we want to insert into the prompt.
    examples=examples,
    # This is how we want to format the examples when we insert them into the prompt.
    example_prompt=example_prompt,
    prefix='Give the antonym of every input\n',
    suffix='Word: {input}\nAntonym: ',
    input_variables=['input'],
    example_separator='\n',
)

print(few_shot_prompt.format(input='big'))
# output:

#Give the antonym of every input
#
#Word: happy
#Antonym: sad
#
#Word: tall
#Antonym: short
#
#Word: big
#Antonym:


