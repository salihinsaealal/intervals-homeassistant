# ![logo@0.5x](assets/logo.png)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Open in HACS](https://img.shields.io/badge/-Add%20with%20HACS-41BDF5?logo=home-assistant&logoColor=white&style=flat-square)](https://my.home-assistant.io/redirect/hacs_repository/?owner=salihinsaealal&repository=intervals-homeassistant&category=integration)
[![Open in Home Assistant](https://img.shields.io/badge/-Open%20in%20Home%20Assistant-41BDF5?logo=home-assistant&logoColor=white&style=flat-square)](https://my.home-assistant.io/redirect/integration/?domain=intervals_icu)
[![GitHub Repo](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white&style=flat-square)](https://github.com/salihinsaealal/intervals-homeassistant)
[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-FFDD00?logo=buy-me-a-coffee&logoColor=black&style=flat-square)](https://coff.ee/salihin)

Integrate your [Intervals.icu](https://intervals.icu/) fitness and training data directly into [Home Assistant](https://www.home-assistant.io/).

---

## Features

- Secure Basic Auth with your Intervals.icu API Key
- **Wellness Sensor**: All your latest wellness metrics
- **Events Sensor**: See your upcoming or past events
- Data updates every 15 minutes
- Easy setup via Home Assistant UI
- HACS-ready for seamless updates

---

## Installation

### HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to the three dots menu (⋮) in the top right
3. Select **Custom repositories**
4. Add this repo URL: `https://github.com/salihinsaealal/intervals-homeassistant`
5. Select category: **Integration**
6. Click **Add**
7. Search for **Intervals.icu** in HACS > Integrations
8. Click **Download**
9. **Restart Home Assistant**

### Manual
1. Copy the `intervals_icu` folder to your `config/custom_components/` directory
2. **Restart Home Assistant**

---

## Configuration

1. Go to **Settings > Devices & Services** in Home Assistant
2. Click **Add Integration** and search for **Intervals.icu**
3. Enter your Intervals.icu **Athlete ID** and **API Key** ([get your API key](https://forum.intervals.icu/t/api-access-to-intervals-icu/609))
4. Complete the setup

---

## Entities and Attributes

### `sensor.intervals_icu_wellness`
- **State:** `readiness` (your readiness score)
- **Attributes:** All fields returned by the Intervals.icu wellness API, for example:

| Attribute         | Description                        |
|-------------------|------------------------------------|
| weight            | Your weight                        |
| restingHR         | Resting heart rate                 |
| hrv               | Heart rate variability             |
| hrvSDNN           | HRV SDNN                           |
| readiness         | Readiness score                    |
| menstrualPhase    | Menstrual phase                    |
| systolic          | Systolic blood pressure            |
| diastolic         | Diastolic blood pressure           |
| bodyFat           | Body fat percentage                |
| water             | Body water percentage              |
| muscleMass        | Muscle mass                        |
| boneMass          | Bone mass                          |
| energy            | Energy level                       |
| hydration         | Hydration level                    |
| mood              | Mood                               |
| soreness          | Soreness level                     |
| stress            | Stress level                       |
| sleepSecs         | Sleep duration (seconds)           |
| spO2              | SpO2 level                         |
| respirationRate   | Respiration rate                   |
| bloodGlucose      | Blood glucose level                |
| lactate           | Lactate level                      |
| bloodPressure     | Blood pressure                     |
| comment           | Any comments                       |

*Note: The actual attributes depend on your data in Intervals.icu.*

### `sensor.intervals_icu_events`
- **State:** Number of events (length of the events list)
- **Attributes:**
  - `events`: List of all event objects returned by the API

### `sensor.intervals_icu_recent_activity`
- **State:** Name of your most recent activity
- **Attributes:** All fields returned by the Intervals.icu activities API for the most recent activity, for example:

| Attribute           | Description                        |
|---------------------|------------------------------------|
| id                  | Activity ID                        |
| name                | Activity name                      |
| type                | Activity type                      |
| description         | Description                        |
| start_date          | Start date/time                    |
| elapsed_time        | Elapsed time (seconds)             |
| distance            | Distance (meters)                  |
| moving_time         | Moving time (seconds)              |
| average_speed       | Average speed                      |
| max_speed           | Max speed                          |
| total_elevation_gain| Total elevation gain               |
| calories            | Calories burned                    |
| ...                 | ... (all other fields from API)    |

*Note: The actual attributes depend on your data in Intervals.icu.*

---

## Example Dashboard

> See [`example_dashboard.yaml`](./example_dashboard.yaml) for a ready-to-use Bubble Card dashboard example for Intervals.icu!

This example uses [Bubble Card](https://github.com/Devqon/bubble-card) for a beautiful, modern UI.  
You can import or copy the YAML from the file directly into your Home Assistant dashboard.

---

## Troubleshooting

- Enable debug logging in `configuration.yaml`:
  ```yaml
  logger:
    default: warning
    logs:
      custom_components.intervals_icu: debug
  ```
- Check your API key and athlete ID are correct
- See [Intervals.icu API docs](https://intervals.icu/api-docs.html) for more info

---

## HACS & Home Assistant Compliance
- [x] `manifest.json` with all required fields
- [x] `info.md` (optional, but recommended)
- [x] Clear install/config instructions
- [x] Entity and attribute documentation
- [x] Example dashboard YAML
- [x] Troubleshooting section
- [x] MIT License

---

## License
MIT
