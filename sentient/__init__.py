from sentient.core.orchestrator.orchestrator import Orchestrator
from sentient.core.agent.agent import Agent
from sentient.core.models.models import State
from sentient.core.memory import ltm

class Sentient:
    def __init__(self):
        self.orchestrator = None
    
    def _create_state_to_agent_map(self, provider: str):
        return {
            State.BASE_AGENT: Agent(provider=provider),
        }

    async def _initialize(self, provider: str, model: str):
        if not self.orchestrator:
            state_to_agent_map = self._create_state_to_agent_map(provider)
            self.orchestrator = Orchestrator(state_to_agent_map=state_to_agent_map, model=model)
            await self.orchestrator.start()

    async def invoke(self, goal: str, provider: str = "openai", model: str = "gpt-4o-2024-08-06", task_instructions: str = None):
        if task_instructions:
            ltm.set_task_instructions(task_instructions)
        await self._initialize(provider, model)
        result = await self.orchestrator.execute_command(goal)
        return result

    async def shutdown(self):
        if self.orchestrator:
            await self.orchestrator.shutdown()

sentient = Sentient()