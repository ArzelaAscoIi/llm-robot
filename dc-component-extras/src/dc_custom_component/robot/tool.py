from __future__ import annotations
from typing import Any, Dict, List
from haystack_experimental.components.tools.openapi import OpenAPITool, LLMProvider
from haystack import component, default_to_dict, default_from_dict
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage


@component
class ChatMessageConverter:
    def __init__(self):
        pass

    @component.output_types(parsed_messages=List[ChatMessage])
    def run(
        self,
        query: str,
    ):
        return {"parsed_messages": [ChatMessage.from_user(query)]}

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChatMessageConverter:
        return cls()


@component
class RobotOpenAPITool(OpenAPITool):
    pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RobotOpenAPITool:
        # secret = None
        # if data["init_parameters"].get("credentials"):
        #     secret = Secret.from_dict(data["init_parameters"]["credentials"])
        # else:
        #     secret = Secret.from_env_var("OPENAI_API_KEY")
        return cls(
            spec="https://raw.githubusercontent.com/ArzelaAscoIi/llm-robot/refs/heads/main/openapi.yaml",
            generator_api=LLMProvider.OPENAI,
            generator_api_params={},
            credentials=None,
        )
