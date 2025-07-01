"""Sensor platform for the Intervals.icu integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IntervalsIcuCoordinator

WELLNESS_SENSORS = {
    "weight": "Weight",
    "restingHR": "Resting HR",
    "hrv": "HRV",
    "hrvSDNN": "HRV SDNN",
    "readiness": "Readiness",
    "menstrualPhase": "Menstrual Phase",
    "systolic": "Systolic",
    "diastolic": "Diastolic",
    "bodyFat": "Body Fat",
    "water": "Water",
    "muscleMass": "Muscle Mass",
    "boneMass": "Bone Mass",
    "energy": "Energy",
    "hydration": "Hydration",
    "mood": "Mood",
    "soreness": "Soreness",
    "stress": "Stress",
    "sleepSecs": "Sleep",
    "spO2": "SpO2",
    "respirationRate": "Respiration Rate",
    "bloodGlucose": "Blood Glucose",
    "lactate": "Lactate",
    "bloodPressure": "Blood Pressure",
    "comment": "Comment",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = IntervalsIcuCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        WellnessSensor(coordinator, entry, key, name)
        for key, name in WELLNESS_SENSORS.items()
    ]
    sensors.append(RecentActivitySensor(coordinator, entry))

    async_add_entities(sensors)


class WellnessSensor(CoordinatorEntity[IntervalsIcuCoordinator], SensorEntity):
    """A sensor for a single wellness data point from Intervals.icu."""

    def __init__(
        self,
        coordinator: IntervalsIcuCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Intervals.icu {name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def native_value(self) -> str | int | float | None:
        """Return the state of the sensor."""
        if self.coordinator.data and "wellness" in self.coordinator.data:
            return self.coordinator.data["wellness"].get(self._key)
        return None


class RecentActivitySensor(CoordinatorEntity[IntervalsIcuCoordinator], SensorEntity):
    """A sensor for the most recent activity from Intervals.icu."""

    def __init__(
        self, coordinator: IntervalsIcuCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Intervals.icu Recent Activity"
        self._attr_unique_id = f"{entry.entry_id}_recent_activity"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if self.coordinator.data and "events" in self.coordinator.data:
            if events := self.coordinator.data["events"]:
                return events[-1].get("name")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str] | None:
        """Return the state attributes."""
        if self.coordinator.data and "events" in self.coordinator.data:
            if events := self.coordinator.data["events"]:
                # Flatten the attributes
                attributes = {}
                for key, value in events[-1].items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            attributes[f"{key}_{sub_key}"] = sub_value
                    else:
                        attributes[key] = value
                return attributes
        return None
