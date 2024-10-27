from __future__ import annotations
from typing import Any, Dict
from haystack_experimental.components.tools.openapi import OpenAPITool, LLMProvider
from haystack import component

# @component
# class ChatMessageConverter:
#     def __init__(self):
#         pass

#     @component.output_types(parsed_messages=List[ChatMessage])
#     def run(
#         self,
#         query: str,
#     ):
#         return {"parsed_messages": [ChatMessage.from_user(query)]}

#     def to_dict(self) -> Dict[str, Any]:
#         return default_to_dict(self)

#     @classmethod
#     def from_dict(cls, data: Dict[str, Any]) -> ChatMessageConverter:
#         return cls()


@component
class RobotOpenAPITool(OpenAPITool):
    def __init__(
        self,
        generator_api: LLMProvider,
        generator_api_params: Dict[str, Any] | None = None,
        spec: str | None = None,
    ) -> None:
        super().__init__(generator_api, generator_api_params, spec)
