# Intervals.icu Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integrate your [Intervals.icu](https://intervals.icu/) fitness and training data directly into [Home Assistant](https://www.home-assistant.io/).

## Features

*   Basic authentication with your Intervals.icu API Key.
*   A sensor for your wellness data.
*   A sensor for your most recent activity.
*   Data updates every 15 minutes.

## Installation

### HACS (Recommended)

1.  Open HACS in your Home Assistant instance
2.  Go to the three dots menu (⋮) in the top right corner
3.  Select "Custom repositories"
4.  Add this repository URL: `https://github.com/salihinsaealal/intervals-homeassistant`
5.  Select category: "Integration"
6.  Click "Add"
7.  Search for "Intervals.icu" in HACS > Integrations
8.  Click "Download"
9.  Restart Home Assistant

### Manual

1.  Copy the `intervals_icu` folder to your `config/custom_components/` directory
2.  Restart Home Assistant

## Configuration

1.  Go to **Settings > Devices & Services** in Home Assistant.
2.  Click **Add Integration** and search for **Intervals.icu**.
3.  Enter your Intervals.icu API Key and Athlete ID.
4.  Complete the setup.

## Entities and Attributes

### `sensor.intervals_icu_wellness`

| State |
| :--- |
| Your current fitness level. |

| Attribute | Description |
| :--- | :--- |
| `weight` | Your weight. |
| `restingHR` | Your resting heart rate. |
| `hrv` | Your heart rate variability. |
| `hrvSDNN` | Your HRV SDNN. |
| `readiness` | Your readiness score. |
| `menstrualPhase` | Your menstrual phase. |
| `systolic` | Your systolic blood pressure. |
| `diastolic` | Your diastolic blood pressure. |
| `bodyFat` | Your body fat percentage. |
| `water` | Your body water percentage. |
| `muscleMass` | Your muscle mass. |
| `boneMass` | Your bone mass. |
| `energy` | Your energy level. |
| `hydration` | Your hydration level. |
| `mood` | Your mood. |
| `soreness` | Your soreness level. |
| `stress` | Your stress level. |
| `sleepSecs` | Your sleep duration in seconds. |
| `spO2` | Your SpO2 level. |
| `respirationRate` | Your respiration rate. |
| `bloodGlucose` | Your blood glucose level. |
| `lactate` | Your lactate level. |
| `bloodPressure` | Your blood pressure. |
| `comment` | Any comments on your wellness. |

### `sensor.intervals_icu_recent_activity`

| State |
| :--- |
| The name of your most recent activity. |

| Attribute | Description |
| :--- | :--- |
| `id` | The activity ID. |
| `start_date_local` | The start date and time of the activity. |
| `icu_training_load` | The training load of the activity. |
| `icu_atl` | Your ATL after the activity. |
| `icu_ctl` | Your CTL after the activity. |
| `calendar_id` | The ID of the calendar the activity belongs to. |
| `uid` | The unique ID of the activity. |
| `category` | The category of the activity. |
| `end_date_local` | The end date and time of the activity. |
| `description` | The description of the activity. |
| `type` | The type of the activity. |
| `color` | The color of the activity in the calendar. |
| `moving_time` | The moving time of the activity in seconds. |
| `icu_ftp` | Your FTP at the time of the activity. |
| `atl_days` | The number of days used to calculate ATL. |
| `ctl_days` | The number of days used to calculate CTL. |
| `updated` | The last time the activity was updated. |

## Example Dashboard YAML

> This example uses the Mushroom Cards custom component for a beautiful, modern UI.

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Intervals.icu
  - type: custom:mushroom-chips-card
    chips:
      - type: entity
        entity: sensor.intervals_icu_wellness
        name: Fitness
      - type: entity
        entity: sensor.intervals_icu_wellness
        name: Resting HR
        icon: mdi:heart-pulse
        use_attribute_as_state: true
        attribute: restingHR
      - type: entity
        entity: sensor.intervals_icu_wellness
        name: Weight
        icon: mdi:weight-kilogram
        use_attribute_as_state: true
        attribute: weight
  - type: custom:mushroom-entity-card
    entity: sensor.intervals_icu_recent_activity
    name: Recent Activity
    icon: mdi:run
    primary_info: state
    secondary_info: attribute
    attribute: start_date_local
```

## Troubleshooting

*   Enable debug logging in `configuration.yaml`:
    ```yaml
    logger:
      default: warning
      logs:
        custom_components.intervals_icu: debug
    ```

## License

MIT
