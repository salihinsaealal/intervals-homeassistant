"""Sensor platform for the Intervals.icu integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    DOMAIN,
    SENSOR_WELLNESS,
    SENSOR_EVENTS,
    CONF_ATHLETE_ID,
)
from .coordinator import IntervalsDataUpdateCoordinator

# Add a constant for the recent activity sensor
SENSOR_RECENT_ACTIVITY = "recent_activity"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Intervals.icu sensor based on a config entry."""
    coordinator: IntervalsDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            IntervalsIcuWellnessSensor(coordinator),
            IntervalsIcuEventsSensor(coordinator),
            IntervalsIcuRecentActivitySensor(coordinator),
        ]
    )


class IntervalsIcuSensor(SensorEntity):
    """Base class for Intervals.icu sensors."""

    def __init__(self, coordinator: IntervalsDataUpdateCoordinator, sensor_type: str) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_type = sensor_type
        self._attr_has_entity_name = True

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class IntervalsIcuWellnessSensor(IntervalsIcuSensor):
    """Representation of Intervals.icu Wellness sensor."""

    def __init__(self, coordinator: IntervalsDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, SENSOR_WELLNESS)
        athlete_id = self.coordinator.athlete_id
        self._attr_name = f"Intervals.icu Wellness {athlete_id}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SENSOR_WELLNESS}"

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data.get("wellness", {})
        return data.get("readiness")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        return self.coordinator.data.get("wellness", {})


class IntervalsIcuEventsSensor(IntervalsIcuSensor):
    """Representation of Intervals.icu Events sensor."""

    def __init__(self, coordinator: IntervalsDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, SENSOR_EVENTS)
        athlete_id = self.coordinator.athlete_id
        self._attr_name = f"Intervals.icu Events {athlete_id}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SENSOR_EVENTS}"

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        data = self.coordinator.data.get("events", [])
        return len(data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        return {"events": self.coordinator.data.get("events", [])}


class IntervalsIcuRecentActivitySensor(IntervalsIcuSensor):
    """Representation of Intervals.icu Recent Activity sensor."""

    def __init__(self, coordinator: IntervalsDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, SENSOR_RECENT_ACTIVITY)
        athlete_id = self.coordinator.athlete_id
        self._attr_name = f"Intervals.icu Recent Activity {athlete_id}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SENSOR_RECENT_ACTIVITY}"

    @property
    def state(self) -> StateType:
        """Return the state of the sensor (activity name)."""
        data = self.coordinator.data.get("recent_activity", {})
        return data.get("name") if data else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return all fields of the recent activity as attributes."""
        return self.coordinator.data.get("recent_activity", {}) or {}
