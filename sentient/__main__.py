import asyncio

from sentient.core.agent.agent import Agent
from sentient.core.models.models import State
from sentient.core.orchestrator.orchestrator import Orchestrator


async def main():
    # Define state machine
    state_to_agent_map = {
        State.BASE_AGENT: Agent(),
    }

    orchestrator = Orchestrator(state_to_agent_map=state_to_agent_map)
    await orchestrator.start()


if __name__ == "__main__":
    asyncio.run(main())
