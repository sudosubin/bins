from typing import Any, Optional

import aiohttp
from aiohttp.typedefs import StrOrURL


class Request:
    """Send http request with aiohttp.

    Attributes:
        _session: aiohttp ClientSession instance
    """
    _session: Optional[aiohttp.ClientSession]

    def __init__(self):
        self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get existing session, or create new session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

        return self._session

    async def get(self, url: StrOrURL, **kwargs: Any):
        """Delegate GET request"""
        response = await self.session.get(url, **kwargs)
        return await response.json()

    def __del__(self):
        if self._session is None:
            return

        if not self._session.closed and self._session._connector is not None and self._session._connector_owner:
            self._session._connector._close()

        self._session = None


request = Request()
