from datetime import datetime
from string import Template

from sentient.core.agent.base import BaseAgent
from sentient.core.memory import ltm
from sentient.core.models.models import AgentInput, AgentOutput
from sentient.core.prompts.prompts import LLM_PROMPTS


class Agent(BaseAgent):
    def __init__(self, provider:str):
        self.name = "sentient"
        self.ltm = None
        self.ltm = self.__get_ltm()
        self.system_prompt = self.__modify_system_prompt(self.ltm)
        super().__init__(
            name=self.name,
            system_prompt=self.system_prompt,
            input_format=AgentInput,
            output_format=AgentOutput,
            keep_message_history=False,
            provider=provider,
        )

    @staticmethod
    def __get_ltm():
        return ltm.get_task_instructions()

    def __modify_system_prompt(self, ltm):
        system_prompt: str = LLM_PROMPTS["BASE_AGENT_PROMPT"]

        substitutions = {
            "task_information": ltm if ltm is not None else "",
        }

        # Use safe_substitute to avoid KeyError
        system_prompt = Template(system_prompt).safe_substitute(substitutions)

        # Add today's day & date to the system prompt
        today = datetime.now()
        today_date = today.strftime("%d/%m/%Y")
        weekday = today.strftime("%A")
        system_prompt += f"\nToday's date is: {today_date}"
        system_prompt += f"\nCurrent weekday is: {weekday}"

        return system_prompt
