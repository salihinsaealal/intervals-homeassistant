"""Data update coordinator for the Intervals.icu integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class IntervalsIcuCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the Intervals.icu integration."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )
        self.session = async_get_clientsession(hass)
        self.api_key = entry.data["api_key"]
        self.athlete_id = entry.data["athlete_id"]
        self.auth = aiohttp.BasicAuth("API_KEY", password=self.api_key)

    async def _async_update_data(self) -> dict:
        """Fetch data from the API."""
        try:
            async with asyncio.timeout(10):
                wellness_response = await self.session.get(
                    f"https://intervals.icu/api/v1/athlete/{self.athlete_id}/wellness",
                    auth=self.auth,
                )
                wellness_response.raise_for_status()
                wellness_data = await wellness_response.json()

                return {
                    "wellness": wellness_data,
                }
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
