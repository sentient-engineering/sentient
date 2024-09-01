import asyncio
import inspect

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from typing_extensions import Annotated

from sentient.core.web_driver.playwright import PlaywrightManager
from sentient.utils.logger import logger


async def openurl(
    url: Annotated[
        str,
        "The URL to navigate to. Value must include the protocol (http:// or https://).",
    ],
    timeout: Annotated[int, "Additional wait time in seconds after initial load."],
    max_retries: Annotated[int, "Maximum number of retry attempts"] = 3,
) -> Annotated[str, "Returns the result of this request in text form"]:
    """
    Opens a specified URL in the active browser instance. Waits for an initial load event, then waits for either
    the 'domcontentloaded' event or a configurable timeout, whichever comes first.

    Parameters:
    - url: The URL to navigate to.
    - timeout: Additional time in seconds to wait after the initial load before considering the navigation successful.
    - max_retries: Maximum number of retry attempts (default: 3).

    Returns:
    - URL of the new page.
    """
    logger.info(f"Opening URL: {url}")
    browser_manager = PlaywrightManager(browser_type="chromium", headless=False)
    await browser_manager.get_browser_context()
    page = await browser_manager.get_current_page()
    # Navigate to the URL with a short timeout to ensure the initial load starts
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    url = ensure_protocol(url)

    for attempt in range(max_retries):
        try:
            await browser_manager.take_screenshots(f"{function_name}_start", page)

            # Use a longer timeout for navigation
            await page.goto(
                url, timeout=max(30000, timeout * 1000), wait_until="domcontentloaded"
            )

            # Wait for network idle to ensure page is fully loaded
            await page.wait_for_load_state(
                "networkidle", timeout=max(30000, timeout * 1000)
            )

            await browser_manager.take_screenshots(f"{function_name}_end", page)

            title = await page.title()
            final_url = page.url
            logger.info(f"Successfully loaded page: {final_url}")
            return f"Page loaded: {final_url}, Title: {title}"

        except PlaywrightTimeoutError as e:
            logger.warning(f"Timeout error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to load {url} after {max_retries} attempts")
                return f"Failed to load page: {url}. Error: Timeout after {max_retries} attempts"
            await asyncio.sleep(2)  # Wait before retrying

        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return f"Failed to load page: {url}. Error: {str(e)}"

    await browser_manager.take_screenshots(f"{function_name}_end", page)

    # await browser_manager.notify_user(
    #     f"Opened URL: {url}", message_type=MessageType.ACTION
    # )
    # Get the page title
    title = await page.title()
    url = page.url
    return f"Page loaded: {url}, Title: {title}"  # type: ignore


def ensure_protocol(url: str) -> str:
    """
    Ensures that a URL has a protocol (http:// or https://). If it doesn't have one,
    https:// is added by default.

    Parameters:
    - url: The URL to check and modify if necessary.

    Returns:
    - A URL string with a protocol.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Default to http if no protocol is specified
        logger.info(
            f"Added 'https://' protocol to URL because it was missing. New URL is: {url}"
        )
    return url
