"""Config flow for Tesla Serve Key."""

import logging
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.persistent_notification import async_create
from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "tesla_serve_key"

_LOGGER = logging.getLogger(__name__)

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
        return self.async_create_entry(title=user_input["name"], data=data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return TeslaServeKeyOptionsFlow()


class TeslaServeKeyOptionsFlow(OptionsFlow):
    """Handle options flow for Tesla Serve Key."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow - check PEM and send notification."""
        
        # Run the check
        file_status = await self._get_pem_status()
        verification = await self._verify_pem()
        
        # Create a notification with results
        message = f"**File Status:**\n{file_status}\n\n**HTTP Verification:**\n{verification['message']}"
        
        # Create persistent notification using the correct import
        async_create(
            self.hass,
            message,
            title="Tesla PEM Verification",
            notification_id="tesla_pem_check",
        )
        
        # Close the options dialog
        return self.async_create_entry(title="", data={})

    async def _verify_pem(self) -> dict[str, Any]:
        """Verify the PEM file is being served."""
        try:
            if self.hass.config.external_url:
                base_url = self.hass.config.external_url
            elif self.hass.config.internal_url:
                base_url = self.hass.config.internal_url
            else:
                base_url = "http://localhost:8123"
            
            pem_url = f"{base_url}/.well-known/appspecific/com.tesla.3p.public-key.pem"
            session = async_get_clientsession(self.hass)
            
            async with session.get(pem_url, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    if "BEGIN PUBLIC KEY" in content and "END PUBLIC KEY" in content:
                        preview = content[:100].replace('\n', ' ')
                        return {
                            "success": True,
                            "message": f"✅ **SUCCESS!**\n\nURL: {pem_url}\n\nHTTP Status: {response.status}\n\nPreview: {preview}...",
                        }
                    return {
                        "success": False,
                        "message": f"❌ **INVALID PEM FORMAT**\n\nURL: {pem_url}\n\nStatus: {response.status}",
                    }
                return {
                    "success": False,
                    "message": f"❌ **NOT ACCESSIBLE**\n\nURL: {pem_url}\n\nHTTP Status: {response.status}",
                }
        except Exception as err:
            _LOGGER.exception("Error verifying PEM")
            return {
                "success": False,
                "message": f"❌ **ERROR**\n\n{err}",
            }

    async def _get_pem_status(self) -> str:
        """Get the current PEM file status."""
        try:
            config_dir = Path(self.hass.config.config_dir)
            pem_locations = [
                config_dir / ".well-known" / "appspecific" / "com.tesla.3p.public-key.pem",
                config_dir / "tesla-public-key.pem",
            ]
            
            for pem_path in pem_locations:
                if pem_path.is_file():
                    return f"📄 **Found:** {pem_path}"
            
            return "⚠️ **NOT FOUND** in config directory\n\nExpected:\n- <config>/.well-known/appspecific/com.tesla.3p.public-key.pem\n- <config>/tesla-public-key.pem"
        except Exception as err:
            _LOGGER.exception("Error checking PEM")
            return f"❌ Error: {err}"
