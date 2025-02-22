from typing import Protocol, runtime_checkable
from huggingface_hub import InferenceClient


@runtime_checkable
class LLM(Protocol):
    def observe(self, prompt: str) -> str: ...

    def think(self, prompt: str, stop: str = "Observation:") -> str: ...


class HuggingFace:
    def __init__(
        self,
        endpoint_url: str = "https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud",
    ):
        self.client = InferenceClient(endpoint_url)

    def observe(self, prompt: str) -> str:
        return self.client.text_generation(
            prompt, max_new_tokens=200, do_sample=True, temperature=0.7
        )

    def think(self, prompt: str, stop: str = "Observation:") -> str:
        return self.client.text_generation(
            prompt,
            max_new_tokens=200,
            stop=[stop],
            do_sample=True,
            temperature=0.7,
        )
