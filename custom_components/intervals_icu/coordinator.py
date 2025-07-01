"""Data update coordinator for the Intervals.icu integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta, datetime
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    API_BASE_URL,
    CONF_ATHLETE_ID,
    CONF_API_KEY,
    ENDPOINT_WELLNESS,
    ENDPOINT_EVENTS,
    ENDPOINT_ACTIVITIES,
)

_LOGGER = logging.getLogger(__name__)


class IntervalsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Intervals.icu API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        config_data: dict[str, Any],
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.session = session
        self.athlete_id = config_data[CONF_ATHLETE_ID]
        self.api_key = config_data[CONF_API_KEY]
        self.auth = aiohttp.BasicAuth("API_KEY", self.api_key)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoints."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            tasks = [
                self._make_api_request(f"wellness/{today}"),
                self._make_api_request(ENDPOINT_EVENTS),
                self._make_api_request(f"{ENDPOINT_ACTIVITIES}?oldest=2000-01-01&limit=1"),
            ]

            wellness_data, events_data, activities_data = await asyncio.gather(*tasks)

            # Get the most recent activity (should be the only one returned)
            recent_activity = activities_data[0] if activities_data and isinstance(activities_data, list) else None

            return {
                "wellness": wellness_data,
                "events": events_data,
                "recent_activity": recent_activity,
            }

        except Exception as err:
            raise UpdateFailed(f"Error communicating with Intervals.icu API: {err}") from err

    async def _make_api_request(self, endpoint: str) -> dict:
        """Make an authenticated API request."""
        url = f"{API_BASE_URL}/athlete/{self.athlete_id}/{endpoint}"

        try:
            async with self.session.get(url, auth=self.auth) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"API request failed: {err}") from err
