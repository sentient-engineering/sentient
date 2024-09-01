import asyncio
from sentient.core.orchestrator.orchestrator import Orchestrator
from sentient.core.agent.agent import Agent
from sentient.core.models.models import State

class Sentient:
    def __init__(self):
        self.state_to_agent_map = {
            State.BASE_AGENT: Agent(),
        }
        self.orchestrator = None

    async def _initialize(self):
        if not self.orchestrator:
            self.orchestrator = Orchestrator(state_to_agent_map=self.state_to_agent_map)
            await self.orchestrator.start()

    async def invoke(self, command: str):
        await self._initialize()
        result = await self.orchestrator.execute_command(command)
        return result

    async def shutdown(self):
        if self.orchestrator:
            await self.orchestrator.shutdown()

sentient = Sentient()

def run(command: str):
    async def _run():
        try:
            result = await sentient.invoke(command)
            return result
        finally:
            await sentient.shutdown()

    return asyncio.run(_run())