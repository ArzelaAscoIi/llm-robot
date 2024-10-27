from __future__ import annotations
from typing import Any, Dict, List
from haystack_experimental.components.tools.openapi import OpenAPITool, LLMProvider
from haystack import component
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
        return {"messages": [ChatMessage.from_user(query)]}


@component
class RobotOpenAPITool(OpenAPITool):
    def __init__(
        self,
        generator_api: LLMProvider,
        generator_api_params: Dict[str, Any] | None = None,
        spec: str | None = None,
    ) -> None:
        super().__init__(generator_api, generator_api_params, spec)
