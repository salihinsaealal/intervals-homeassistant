"""Constants for the Intervals.icu integration."""

from datetime import timedelta

DOMAIN = "intervals_icu"
API_BASE_URL = "https://intervals.icu/api/v1"
ENDPOINT_WELLNESS = "wellness"
ENDPOINT_EVENTS = "events"
ENDPOINT_ACTIVITIES = "activities"
CONF_ATHLETE_ID = "athlete_id"
CONF_API_KEY = "api_key"
UPDATE_INTERVAL = timedelta(minutes=15)
