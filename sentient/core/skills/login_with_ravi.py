from typing import Annotated
from sentient.ravi.ravi import Ravi
from sentient.core.web_driver.playwright import PlaywrightManager
from sentient.utils.logger import logger

async def login(
    api_key: Annotated[str, "The API key for authentication with Ravi service"],
    domain: Annotated[str, "The domain of the website to authenticate"],
    user_id: Annotated[str, "The user ID for authentication"]
) -> Annotated[str, "A message indicating success or failure of the login attempt"]:
    """
    Attempts to log in to a website using the Ravi authentication service.

    This function retrieves authentication context from Ravi and applies it to the current browser session.
    It then refreshes the page to ensure the login state is applied.

    Parameters:
    - api_key: The API key for authentication with Ravi service
    - domain: The domain of the website to authenticate
    - user_id: The user ID for authentication

    Returns:
    - A string message indicating the success or failure of the login attempt
    """
    logger.info(f"Attempting to login to {domain} using Ravi authentication service")

    try:
        # Get the remote context from Ravi
        remote_context = await Ravi.get_remote_context(domain, api_key, user_id)

        if not remote_context:
            return "Login failed: Unable to retrieve authentication context from Ravi"

        # Get the current page from PlaywrightManager
        browser_manager = PlaywrightManager()
        page = await browser_manager.get_current_page()

        if not page:
            return "Login failed: No active page found"

        # Apply the remote context to the current page
        await page.context.add_cookies(remote_context.get('cookies', []))
        await page.context.add_storage_state(remote_context.get('origins', {}))

        # Refresh the page to apply the new authentication state
        await page.reload()

        # Check if login was successful (this is a basic check, you might want to customize it)
        if "login" not in page.url.lower() and "sign in" not in page.url.lower():
            return f"Login successful for domain: {domain}"
        else:
            return f"Login might have failed for domain: {domain}. Please verify the current page."

    except Exception as e:
        logger.error(f"Error during login process: {str(e)}")
        return f"Login failed: An error occurred - {str(e)}"
