"""Config flow for Tesla Serve Key.

This only asks for a friendly name; endpoint path and auth are fixed and not configurable.
"""

import voluptuous as vol

from homeassistant import config_entries

from . import DOMAIN

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Tesla Serve Key"): str,
    }
)


class TeslaServeKeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tesla Serve Key."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)

        data = {"name": user_input["name"]}
        # No options are stored for endpoint path since it's fixed.
        return self.async_create_entry(title=user_input["name"], data=data)
