import asyncio
import textwrap
import uuid
from typing import Dict, List

from colorama import Fore, init
from dotenv import load_dotenv
from langsmith import traceable

from sentient.core.agent.base import BaseAgent
from sentient.core.models.models import (
    Action,
    ActionType,
    AgentInput,
    AgentOutput,
    Memory,
    State,
    Task,
)
from sentient.core.skills.click_using_selector import click
from sentient.core.skills.enter_text_using_selector import EnterTextEntry, entertext
from sentient.core.skills.get_dom_with_content_type import get_dom_with_content_type
from sentient.core.skills.get_url import geturl
from sentient.core.skills.open_url import openurl
from sentient.core.skills.enter_text_and_click import enter_text_and_click
from sentient.core.web_driver.playwright import PlaywrightManager

init(autoreset=True)


class Orchestrator:
    def __init__(
        self, state_to_agent_map: Dict[State, BaseAgent], eval_mode: bool = False, model:str = None
    ):
        load_dotenv()
        self.state_to_agent_map = state_to_agent_map
        self.playwright_manager = PlaywrightManager()
        self.eval_mode = eval_mode
        self.shutdown_event = asyncio.Event()
        self.session_id = str(uuid.uuid4())
        self.model = model

    async def start(self):
        print("Starting orchestrator")
        await self.playwright_manager.async_initialize(eval_mode=self.eval_mode)
        print("Browser started and ready")

        # if not self.eval_mode:
        #     await self._command_loop()
    
    @classmethod
    async def invoke(cls, command: str):
        orchestrator = cls()
        await orchestrator.start()
        result = await orchestrator.execute_command(command)
        return result

    async def _command_loop(self):
        while not self.shutdown_event.is_set():
            try:
                command = await self._get_user_input()
                if command.strip().lower() == "exit":
                    await self.shutdown()
                else:
                    await self.execute_command(command)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    async def _get_user_input(self):
        return await asyncio.get_event_loop().run_in_executor(
            None, input, "Enter your command (or type 'exit' to quit) "
        )

    # @traceable(run_type="chain", name="execute_command")
    async def execute_command(self, command: str):
        try:
            # Create initial memory
            self.memory = Memory(
                objective=command,
                current_state=State.BASE_AGENT,
                plan=[],
                thought="",
                completed_tasks=[],
                current_task=None,
                final_response=None,
            )
            print(f"Executing command {self.memory.objective}")
            while self.memory.current_state != State.COMPLETED:
                await self._handle_state()
            self._print_final_response()
            return self.memory.final_response
        except Exception as e:
            print(f"Error executing the command {self.memory.objective}: {e}")

    def run(self) -> Memory:
        while self.memory.current_state != State.COMPLETED:
            self._handle_state()

        self._print_final_response()
        return self.memory

    async def _handle_state(self):
        current_state = self.memory.current_state

        if current_state not in self.state_to_agent_map:
            raise ValueError(f"Unhandled state! No agent for {current_state}")
        
        if current_state == State.BASE_AGENT:
            await self._handle_agnet()
        else:
            raise ValueError(f"Unhandled state: {current_state}")


    async def _handle_agnet(self):
        agent = self.state_to_agent_map[State.BASE_AGENT]
        self._print_memory_and_agent(agent.name)

        # repesenting state with dom representation
        dom = await get_dom_with_content_type(content_type="all_fields")
        url = await geturl()

        input_data = AgentInput(
            objective=self.memory.objective,
            completed_tasks=self.memory.completed_tasks,
            current_page_url=str(url),
            current_page_dom=str(dom),
        )

        output: AgentOutput = await agent.run(
            input_data, session_id=self.session_id, model=self.model
        )

        await self._update_memory_from_agent(output)

        print(f"{Fore.MAGENTA}Base Agent Q has updated the memory.")


    async def _update_memory_from_agent(self, agentq_output: AgentOutput):
        if agentq_output.is_complete:
            self.memory.current_state = State.COMPLETED
            self.memory.final_response = agentq_output.final_response
        elif agentq_output.next_task:
            self.memory.current_state = State.BASE_AGENT
            if agentq_output.next_task_actions:
                action_results = await self.handle_agent_actions(
                    agentq_output.next_task_actions
                )
                print("Action results:", action_results)
                flattened_results = "; ".join(action_results)
                agentq_output.next_task.result = flattened_results

            self.memory.completed_tasks.append(agentq_output.next_task)
            self.memory.plan = agentq_output.plan
            self.memory.thought = agentq_output.thought
            current_task_id = len(self.memory.completed_tasks) + 1
            self.memory.current_task = Task(
                id=current_task_id,
                description=agentq_output.next_task.description,
                url=None,
                result=None,
            )
        else:
            raise ValueError("Planner did not provide next task or completion status")

    async def handle_agent_actions(self, actions: List[Action]):
        results = []
        for action in actions:
            if action.type == ActionType.GOTO_URL:
                result = await openurl(url=action.website, timeout=action.timeout or 1)
                print("Action - GOTO")
            elif action.type == ActionType.TYPE:
                entry = EnterTextEntry(
                    query_selector=f"[mmid='{action.mmid}']", text=action.content
                )
                result = await entertext(entry)
                print("Action - TYPE")
            elif action.type == ActionType.CLICK:
                result = await click(
                    selector=f"[mmid='{action.mmid}']",
                    wait_before_execution=action.wait_before_execution or 1,
                )
                print("Action - CLICK")
            elif action.type == ActionType.ENTER_TEXT_AND_CLICK:
                result = await enter_text_and_click(
                    text_selector=f"[mmid='{action.text_element_mmid}']",
                    text_to_enter=action.text_to_enter,
                    click_selector=f"[mmid='{action.click_element_mmid}']",
                    wait_before_click_execution=action.wait_before_click_execution
                    or 1.5,
                )
                print("Action - ENTER TEXT AND CLICK")
            else:
                result = f"Unsupported action type: {action.type}"

            results.append(result)

        return results

    async def shutdown(self):
        print("Shutting down orchestrator!")
        self.shutdown_event.set()
        await self.playwright_manager.stop_playwright()

    def _print_memory_and_agent(self, agent_type: str):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Current State: {Fore.GREEN}{self.memory.current_state}")
        print(f"{Fore.YELLOW}Agent: {Fore.GREEN}{agent_type}")
        print(f"{Fore.YELLOW}Current Thought: {Fore.GREEN}{self.memory.thought}")
        if len(self.memory.plan) == 0:
            print(f"{Fore.YELLOW}Plan:{Fore.GREEN} none")
        else:
            print(f"{Fore.YELLOW}Plan:")
            for task in self.memory.plan:
                print(f"{Fore.GREEN} {task.id}. {task.description}")
        if self.memory.current_task:
            print(
                f"{Fore.YELLOW}Current Task: {Fore.GREEN}{self.memory.current_task.description}"
            )
        if len(self.memory.completed_tasks) == 0:
            print(f"{Fore.YELLOW}Completed Tasks:{Fore.GREEN} none")
        else:
            print(f"{Fore.YELLOW}Completed Tasks:")
            for task in self.memory.completed_tasks:
                status = "✓" if task.result else " "
                print(f"{Fore.GREEN}  [{status}] {task.id}. {task.description}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_task_result(self, task: Task):
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Task Completed: {Fore.GREEN}{task.description}")
        print(f"{Fore.YELLOW}Result:")
        wrapped_result = textwrap.wrap(task.result, width=80)
        for line in wrapped_result:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.CYAN}{'='*50}")

    def _print_final_response(self):
        print(f"\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}Objective Completed!")
        print(f"{Fore.GREEN}{'='*50}")
        print(f"{Fore.YELLOW}Final Response:")
        wrapped_response = textwrap.wrap(self.memory.final_response, width=80)
        for line in wrapped_response:
            print(f"{Fore.WHITE}{line}")
        print(f"{Fore.GREEN}{'='*50}")
