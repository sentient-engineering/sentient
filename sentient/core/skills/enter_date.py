import asyncio

from typing_extensions import Annotated
from sentient.core.web_driver.playwright import PlaywrightManager
from sentient.core.skills.click_using_selector import do_click
from sentient.utils.logger import logger


async def select_date_from_datepicker(
    date_selector: Annotated[
        str,
        "The DOM selector for the date picker input element, e.g., [mmid='1234']. This is where the date picker will be opened.",
    ],
    target_date: Annotated[
        str,
        "The target date to select in the format 'YYYY-MM-DD'."
    ],
    next_button_selector: Annotated[
        str,
        "The DOM selector for the next month button, e.g., [mmid='5678']. This is used to navigate to the desired month."
    ],
    prev_button_selector: Annotated[
        str,
        "The DOM selector for the previous month button, e.g., [mmid='5679']. This is used to navigate to the desired month."
    ],
    month_year_selector: Annotated[
        str,
        "The DOM selector for the element displaying the current month and year in the date picker, e.g., [mmid='6789']."
    ],
    day_selector_pattern: Annotated[
        str,
        "The DOM selector pattern for selecting a specific day in the date picker, e.g., [mmid='{day}']. The '{day}' will be replaced with the day number."
    ]
) -> Annotated[
    str, "A message indicating success or failure of the date selection."
]:
    """
    Selects a date from a date picker by opening the date picker, navigating to the correct month and year, and selecting the appropriate day.

    Parameters:
    - date_selector: The selector for the date picker input element.
    - target_date: The date to select in 'YYYY-MM-DD' format.
    - next_button_selector: The selector for the next month button.
    - prev_button_selector: The selector for the previous month button.
    - month_year_selector: The selector for the current month and year display.
    - day_selector_pattern: The selector pattern for the days. '{day}' will be replaced by the day number to select the correct day.

    Returns:
    - A message indicating the success or failure of the date selection.
    """
    logger.info(f"Initiating date selection for '{target_date}'.")

    # Initialize PlaywrightManager and get the active browser page
    browser_manager = PlaywrightManager(browser_type="chromium", headless=False)
    page = await browser_manager.get_current_page()
    if page is None:
        error_message = "No active page found."
        logger.error(error_message)
        raise ValueError(error_message)

    # Parse the target date
    target_year, target_month, target_day = map(int, target_date.split('-'))
    logger.info(f"Parsed target date as: Year={target_year}, Month={target_month}, Day={target_day}")

    # Step 1: Click the date picker to open it
    logger.info(f"Clicking on the date picker input using selector: {date_selector}")
    await do_click(page, date_selector)
    await asyncio.sleep(1)  # Wait for the date picker to appear
    logger.info("Date picker opened.")

    # Step 2: Navigate to the correct month and year
    while True:
        # Get the currently displayed month and year
        logger.info(f"Fetching current displayed month and year using selector: {month_year_selector}")
        displayed_month_year = await page.locator(month_year_selector).inner_text()
        displayed_month, displayed_year = displayed_month_year.split(' ')
        displayed_year = int(displayed_year)
        logger.info(f"Currently displayed: {displayed_month} {displayed_year}")

        # Convert displayed month to a number
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
            'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
            'November': 11, 'December': 12
        }
        displayed_month_num = month_map[displayed_month]

        # Check if we're at the target month and year
        if displayed_year == target_year and displayed_month_num == target_month:
            logger.info(f"Target month and year ({target_month}/{target_year}) reached.")
            break
        elif (displayed_year > target_year) or (displayed_year == target_year and displayed_month_num > target_month):
            # Navigate to the previous month
            logger.info(f"Navigating to the previous month using selector: {prev_button_selector}")
            await do_click(page, prev_button_selector)
        else:
            # Navigate to the next month
            logger.info(f"Navigating to the next month using selector: {next_button_selector}")
            await do_click(page, next_button_selector)

        await asyncio.sleep(0.5)  # Small delay to wait for the UI to update

    # Step 3: Select the correct day
    day_selector = day_selector_pattern.replace('{day}', str(target_day))
    logger.info(f"Selecting the day: {target_day} using selector: {day_selector}")
    await do_click(page, day_selector)

    await asyncio.sleep(0.5)  # Wait for the date to be selected
    logger.info(f"Successfully selected the date: {target_date}")
    return f"Successfully selected the date: {target_date}"
