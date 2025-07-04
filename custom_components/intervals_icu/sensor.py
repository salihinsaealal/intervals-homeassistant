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
            IntervalsIcuWellnessDetailsSensor(coordinator),
            IntervalsIcuEventsSensor(coordinator),
            IntervalsIcuRecentActivitySensor(coordinator),
            IntervalsIcuRecentActivityDetailsSensor(coordinator),
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
        self._attr_state_class = "measurement"
        self._attr_device_class = None

    @property
    def state(self) -> StateType:
        """Return the state of the sensor as (ctl-atl)/ctl*100%."""
        data = self.coordinator.data.get("wellness", {})
        ctl = data.get("ctl")
        atl = data.get("atl")
        if ctl is not None and atl is not None and ctl != 0:
            try:
                value = (ctl - atl) / ctl * 100
                return round(value, 1)
            except Exception:
                return None
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data.get("wellness", {})
        # Only expose key metrics
        return {
            "ctl": data.get("ctl"),
            "atl": data.get("atl"),
            "form": data.get("form"),
            "fatigue": data.get("fatigue"),
            "fitness": data.get("fitness"),
            "readiness": data.get("readiness"),
        }


class IntervalsIcuWellnessDetailsSensor(IntervalsIcuSensor):
    """Details sensor for Intervals.icu Wellness (all attributes)."""
    def __init__(self, coordinator: IntervalsDataUpdateCoordinator) -> None:
        super().__init__(coordinator, f"{SENSOR_WELLNESS}_details")
        athlete_id = self.coordinator.athlete_id
        self._attr_name = f"Intervals.icu Wellness Details {athlete_id}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SENSOR_WELLNESS}_details"
        self._attr_state_class = None
        self._attr_device_class = None

    @property
    def state(self) -> StateType:
        return "OK" if self.coordinator.data.get("wellness") else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
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
        data = self.coordinator.data.get("recent_activity", {})
        # Only expose key activity details
        return {
            "name": data.get("name"),
            "date": data.get("date"),
            "type": data.get("type"),
            "duration": data.get("duration"),
            "distance": data.get("distance"),
            "work": data.get("work"),
            "intensity": data.get("intensity"),
        }


class IntervalsIcuRecentActivityDetailsSensor(IntervalsIcuSensor):
    """Details sensor for Intervals.icu Recent Activity (all attributes)."""
    def __init__(self, coordinator: IntervalsDataUpdateCoordinator) -> None:
        super().__init__(coordinator, f"{SENSOR_RECENT_ACTIVITY}_details")
        athlete_id = self.coordinator.athlete_id
        self._attr_name = f"Intervals.icu Recent Activity Details {athlete_id}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{SENSOR_RECENT_ACTIVITY}_details"
        self._attr_state_class = None
        self._attr_device_class = None

    @property
    def state(self) -> StateType:
        return "OK" if self.coordinator.data.get("recent_activity") else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.coordinator.data.get("recent_activity", {}) or {}
