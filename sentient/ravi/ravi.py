from typing import Dict, Any, Optional, Tuple
import aiohttp
import asyncio
from enum import Enum

class RaviResponseStatus(Enum):
    SUCCESS = "success"
    RETRY = "retry"
    LOGIN_FAILED = "login_failed"

class Ravi:

    @classmethod
    async def get_remote_context(cls, domain: str, api_key: str, user_id: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        for attempt in range(max_retries):
            response_data = await cls._make_api_request(domain, api_key, user_id)
            result = cls._handle_api_response(response_data)
            
            if isinstance(result, dict):
                return result
            elif isinstance(result, int):
                await asyncio.sleep(result)
            else:
                raise Exception("Login failed. Unable to complete the request.")

        raise Exception(f"Max retries ({max_retries}) reached. Unable to get remote context.")

    @classmethod
    async def _make_api_request(cls, domain: str, api_key: str, user_id: str) -> Dict[str, Any]:
        url = "https://api.ravi.app/get_context"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "domain": domain,
            "user_id": user_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get remote context: {response.status} {await response.text()}")

    @classmethod
    def _handle_api_response(cls, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[int]]:
        status = RaviResponseStatus(data.get('status'))

        if status == RaviResponseStatus.SUCCESS:
            return data.get('context')
        elif status == RaviResponseStatus.RETRY:
            return data.get('retry_after', 5)  # Default to 5 seconds if not specified
        elif status == RaviResponseStatus.LOGIN_FAILED:
            return None

        raise Exception(f"Unknown status: {status}")
