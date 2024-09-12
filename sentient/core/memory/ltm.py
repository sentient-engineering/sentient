import os

from sentient.config.config import TASK_INSTRUCTION_PATH
from sentient.utils.logger import logger

task_instruction_file_name = "task_instructions.txt"
task_instruction_file = os.path.join(
        TASK_INSTRUCTION_PATH, task_instruction_file_name
    )

def get_task_instructions():
    try:
        with open(task_instruction_file) as file:
            user_pref = file.read()
        logger.info(f"Task instructions loaded from: {task_instruction_file}")
        return user_pref
    except FileNotFoundError:
        logger.warning(f"Task instruction file not found: {task_instruction_file}")

    return None

def set_task_instructions(instructions: str):
    try:
        # clear and write new instructions
        with open(task_instruction_file, 'w') as file:
            file.write(instructions)
        logger.info(f"Task instructions updated in: {task_instruction_file}")
    except IOError:
        logger.error(f"Failed to write task instructions to: {task_instruction_file}")