import os
from smolagents import CodeAgent, TransformersModel
from skyscope_sentinel.memory.manager import MemoryManager
from skyscope_sentinel.tools.os_tools import sys_optimize, manage_service, launch_app, read_pdf
from skyscope_sentinel.tools.quantum_tools import quantum_plan
from skyscope_sentinel.tools.security_tools import firewall_guard, kernel_audit

class SentinelAgent:
    def __init__(self):
        self.memory = MemoryManager()

        # System prompt defining the agent's identity and capabilities
        sys_prompt = (
            "You are SkyScope Sentinel, a persistent multimodal OS assistant designed by Miss Casey Jay Topojani.\n"
            "Capabilities: perception across text, image, audio, and video; analytic modeling; autonomous decision-making; "
            "system optimization through sysctl/systemctl; software management; browser and app automation; learning through "
            "episodic associative memory; and self-reflexive reasoning. You serve as an operator partner capable of creative "
            "concept design and implementation refinement.\n"
            "When conceiving new optimizations or architectures, propose them interactively to the operator via text output "
            "and wait for approval.\n"
        )

        # Initialize the core LLM for local operation
        model = TransformersModel(model_id="HuggingFaceTB/SmolLM-135M-Instruct")

        # Define the agent with its tools and instructions
        self.agent = CodeAgent(
            model=model,
            tools=[
                self.memory.recall_associative,
                sys_optimize,
                manage_service,
                launch_app,
                read_pdf,
                quantum_plan,
                firewall_guard,
                kernel_audit,
            ],
            additional_authorized_imports=["os", "subprocess", "pandas", "numpy"],
            instructions=sys_prompt,
            max_steps=50,
            verbosity_level=2
        )

    def run_task(self, task: str) -> str:
        """Run a task through the agent and log the interaction."""
        result = self.agent.run(task)
        self.memory.log_event("text", task, result)
        return result

    def shutdown(self):
        """Synchronize memory before shutting down."""
        print("🌀 Synchronizing memory...")
        self.memory.sync()