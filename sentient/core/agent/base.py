import json
from typing import Callable, List, Optional, Tuple, Type

import instructor
import instructor.patch
import openai
from instructor import Mode
from langsmith import traceable
from pydantic import BaseModel

from sentient.utils.function_utils import get_function_schema
from sentient.utils.logger import logger
from sentient.utils.providers import get_provider, LLMProvider

class BaseAgent:
    def __init__(
        self,
        name: str,
        system_prompt: str,
        input_format: Type[BaseModel],
        output_format: Type[BaseModel],
        tools: Optional[List[Tuple[Callable, str]]] = None,
        keep_message_history: bool = True,
        provider: str = "openai",
    ):
        # Metdata
        self.agent_name = name

        # Messages
        self.system_prompt = system_prompt
        if self.system_prompt:
            self._initialize_messages()
        self.keep_message_history = keep_message_history

        # Input-output format
        self.input_format = input_format
        self.output_format = output_format

        # Llm client
        self.provider: LLMProvider = get_provider(provider)
        client_config = self.provider.get_client_config()
        self.client = openai.Client(**client_config)
        self.client = instructor.from_openai(self.client, mode=Mode.JSON)

        # Tools
        self.tools_list = []
        self.executable_functions_list = {}
        if tools:
            self._initialize_tools(tools)

    def _initialize_tools(self, tools: List[Tuple[Callable, str]]):
        for func, func_desc in tools:
            self.tools_list.append(get_function_schema(func, description=func_desc))
            self.executable_functions_list[func.__name__] = func

    def _initialize_messages(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    # @traceable(run_type="chain", name="agent_run")
    async def run(
        self, input_data: BaseModel, screenshot: str = None, model:str= None, session_id: str = None
    ) -> BaseModel:
        if not isinstance(input_data, self.input_format):
            raise ValueError(f"Input data must be of type {self.input_format.__name__}")

        # Handle message history.
        if not self.keep_message_history:
            self._initialize_messages()

        if screenshot:
            self.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": input_data.model_dump_json(
                                exclude={"current_page_dom", "current_page_url"}
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": screenshot}},
                    ],
                }
            )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": input_data.model_dump_json(
                        exclude={"current_page_dom", "current_page_url"}
                    ),
                }
            )

        # input dom and current page url in a separate message so that the LLM can pay attention to completed tasks better. *based on personal vibe check*
        if hasattr(input_data, "current_page_dom") and hasattr(
            input_data, "current_page_url"
        ):
            self.messages.append(
                {
                    "role": "user",
                    "content": f"Current page URL:\n{input_data.current_page_url}\n\n Current page DOM:\n{input_data.current_page_dom}",
                }
            )

        while True:
            # TODO:
            # 1. better exeception handling and messages while calling the client
            # 2. remove the else block as JSON mode in instrutor won't allow us to pass in tools.
            # 3. add a max_turn here to prevent a inifinite fallout
            try:
                if len(self.tools_list) == 0:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=self.messages,
                        response_model=self.output_format,
                        max_retries=3,
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=self.messages,
                        response_model=self.output_format,
                        tool_choice="auto",
                        tools=self.tools_list,
                    )

                # instructor directly outputs response.choices[0].message. so we will do response_message = response
                # response_message = response.choices[0].message

                # instructor does not support funciton in JSON mode
                # if response_message.tool_calls:
                #     tool_calls = response_message.tool_calls

                # if tool_calls:
                #     self.messages.append(response_message)
                #     for tool_call in tool_calls:
                #         await self._append_tool_response(tool_call)
                #     continue

                # parsed_response_content: self.output_format = response_message.parsed
                
                assert isinstance(response, self.output_format)
                return response
            except AssertionError:
                    raise TypeError(
                        f"Expected response_message to be of type {self.output_format.__name__}, but got {type(response).__name__}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise

            

    async def _append_tool_response(self, tool_call):
        function_name = tool_call.function.name
        function_to_call = self.executable_functions_list[function_name]
        function_args = json.loads(tool_call.function.arguments)
        try:
            function_response = await function_to_call(**function_args)
            # print(function_response)
            self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )
        except Exception as e:
            logger.error(f"Error occurred calling the tool {function_name}: {str(e)}")
            self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(
                        "The tool responded with an error, please try again with a different tool or modify the parameters of the tool",
                        function_response,
                    ),
                }
            )
