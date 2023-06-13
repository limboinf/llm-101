from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from typing import Optional, List, Any, Mapping

# https://python.langchain.com/en/latest/modules/models/llms/examples/custom_llm.html


class CustomLLM(LLM):

    n: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        return prompt[:self.n]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"n": self.n}

llm = CustomLLM(n = 5)
output = llm('greate job tom')
print(output)
print(llm)