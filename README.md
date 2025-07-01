# Intervals.icu Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Integrate your [Intervals.icu](https://intervals.icu/) fitness and training data directly into [Home Assistant](https://www.home-assistant.io/).

## Features

*   Basic authentication with your Intervals.icu API Key.
*   Sensors for your wellness data.
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

### Wellness Sensors

This integration creates individual sensors for each of the following wellness data points:

*   Weight
*   Resting HR
*   HRV
*   HRV SDNN
*   Readiness
*   Menstrual Phase
*   Systolic
*   Diastolic
*   Body Fat
*   Water
*   Muscle Mass
*   Bone Mass
*   Energy
*   Hydration
*   Mood
*   Soreness
*   Stress
*   Sleep
*   SpO2
*   Respiration Rate
*   Blood Glucose
*   Lactate
*   Blood Pressure
*   Comment

### `sensor.intervals_icu_recent_activity`

**State:** The name of your most recent activity.

**Attributes:** All the data for your most recent activity from the Intervals.icu API, with nested data flattened.

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
