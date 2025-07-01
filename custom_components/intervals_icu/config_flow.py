"""Config flow for Intervals.icu integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    API_BASE_URL,
    CONF_ATHLETE_ID,
)

_LOGGER = logging.getLogger(__name__)


class IntervalsIcuConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Intervals.icu."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                await self._validate_credentials(
                    user_input[CONF_ATHLETE_ID], user_input[CONF_API_KEY]
                )

                await self.async_set_unique_id(user_input[CONF_ATHLETE_ID])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Intervals.icu {user_input[CONF_ATHLETE_ID]}",
                    data=user_input,
                )

            except aiohttp.ClientError as err:
                _LOGGER.error("Connection error: %s", err)
                errors["base"] = "cannot_connect"
            except Exception as err:
                _LOGGER.error("Authentication error: %s", err)
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ATHLETE_ID): str,
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
        )

    async def _validate_credentials(self, athlete_id: str, api_key: str) -> None:
        """Validate the user credentials with Intervals.icu API."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_BASE_URL}/athlete/{athlete_id}/wellness",
                auth=aiohttp.BasicAuth("API_KEY", api_key),
            ) as response:
                if response.status != 200:
                    raise Exception(f"Authentication failed: {response.status}")
