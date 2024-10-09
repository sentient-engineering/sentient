from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field

#Global
class State(str, Enum):
    COMPLETED = "completed"
    BASE_AGENT = "agentq_base"


class ActionType(str, Enum):
    CLICK = "CLICK"
    TYPE = "TYPE"
    GOTO_URL = "GOTO_URL"
    ENTER_TEXT_AND_CLICK = "ENTER_TEXT_AND_CLICK"
    ENTER_DATE = "ENTER_DATE"


class ClickAction(BaseModel):
    type: Literal[ActionType.CLICK] = Field(
        description="""Executes a click action on the element matching the given mmid attribute value. MMID is always a number. Returns Success if click was successful or appropriate error message if the element could not be clicked."""
    )
    mmid: int = Field(
        description="The mmid number of the element that needs to be clicked e.g. 114. mmid will always be a number"
    )
    wait_before_execution: Optional[float] = Field(
        description="Optional wait time in seconds before executing the click event logic"
    )


class TypeAction(BaseModel):
    type: Literal[ActionType.TYPE] = Field(
        description="""Single enter given text in the DOM element matching the given mmid attribute value. This will only enter the text and not press enter or anything else.
   Returns Success if text entry was successful or appropriate error message if text could not be entered."""
    )
    mmid: int = Field(
        description="The mmid number of the element that needs to be clicked e.g. 114. mmid will always be a number"
    )
    content: str = Field(
        description="The text to enter in the element identified by the query_selector."
    )


class GotoAction(BaseModel):
    type: Literal[ActionType.GOTO_URL] = Field(
        description="Opens a specified URL in the web browser instance. Returns url of the new page if successful or appropriate error message if the page could not be opened."
    )
    website: str = Field(
        description="The URL to navigate to. Value must include the protocol (http:// or https://)."
    )
    timeout: Optional[float] = Field(
        description="Additional wait time in seconds after initial load."
    )

class EnterTextAndClickAction(BaseModel):
    type: Literal[ActionType.ENTER_TEXT_AND_CLICK] = Field(
        description="""Enters text into a specified element and clicks another element, both identified by their mmid. Ideal for seamless actions like submitting search queries, this integrated approach ensures superior performance over separate text entry and click commands. Successfully completes when both actions are executed without errors, returning True; otherwise, it provides False or an explanatory message of any failure encountered."""
    )
    text_element_mmid: int = Field(
        description="The mmid number of the element where the text will be entered"
    )
    text_to_enter: str = Field(
        description="The text that will be entered into the element specified by text_element_mmid"
    )
    click_element_mmid: int = Field(
        description="The mmid number of the element that will be clicked after text entry."
    )
    wait_before_click_execution: Optional[float] = Field(
        description="Optional wait time in seconds before executing the click event logic"
    )

# class EnterDateAction(BaseModel):
#     type: Literal[ActionType.ENTER_DATE] = Field(
#         description="""Interacts with a date picker to select a specific date. It clicks on the date picker input to open the calendar, navigates through months using 'Next' or 'Previous' buttons to reach the correct month and year, and selects the desired day. Successfully completes when the correct date is selected; otherwise, it returns an error message indicating the failure."""
#     )
#     date_selector_mmid: int = Field(
#         description="The mmid number of the date picker input element that opens the calendar"
#     )
#     target_date: str = Field(
#         description="The target date to be selected in the format 'YYYY-MM-DD'"
#     )
#     next_button_mmid: int = Field(
#         description="The mmid number of the 'Next Month' button in the date picker"
#     )
#     prev_button_mmid: int = Field(
#         description="The mmid number of the 'Previous Month' button in the date picker"
#     )
#     month_year_selector_mmid: int = Field(
#         description="The mmid number of the element displaying the current month and year in the date picker"
#     )
#     day_selector_pattern: str = Field(
#         description="A selector pattern with {day} placeholder to select the correct day in the calendar"
#     )
#     wait_before_navigation: Optional[float] = Field(
#         description="Optional wait time in seconds before navigating between months"
#     )

Action = Union[
    ClickAction,
    TypeAction,
    GotoAction,
    EnterTextAndClickAction,
    #EnterDateAction
]


class Task(BaseModel):
    id: int
    description: str
    url: Optional[str] = Field(default=None, description="Optional URL of the page on which task will happen")
    result: Optional[str] = Field(default=None, description="Optional result of the task")


class TaskWithActions(BaseModel):
    id: int
    description: str
    actions_to_be_performed: Optional[List[Action]] = Field(default=None)
    result: Optional[str] = Field(default=None)


class Memory(BaseModel):
    objective: str
    current_state: State
    plan: Optional[Union[List[Task], List[TaskWithActions]]] = Field(default=None)
    thought: str
    completed_tasks: Optional[Union[List[Task], List[TaskWithActions]]] = Field(default=None)
    current_task: Optional[Union[Task, TaskWithActions]] = Field(default=None)
    final_response: Optional[str] = Field(default=None)

    class Config:
        use_enum_values = True



# Agent
class AgentInput(BaseModel):
    objective: str
    completed_tasks: Optional[List[Task]] = Field(default=None)
    current_page_url: str
    current_page_dom: str

class AgentOutput(BaseModel):
    thought: str
    plan: List[Task]
    next_task: Optional[Task] = Field(default=None, description="The next task to be executed")
    next_task_actions: Optional[List[Action]] = Field(default=None, description="List of actions for the next task")
    is_complete: bool
    final_response: Optional[str] = Field(default=None, description="Final response of the agent")