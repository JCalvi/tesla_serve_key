"""Tesla Serve Key integration for Home Assistant.

This integration serves the Tesla public key at the well-known path required by Tesla.
"""

import logging
import os
from pathlib import Path

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "tesla_serve_key"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Tesla Serve Key integration from YAML (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tesla Serve Key from a config entry."""
    # Register the view to serve the PEM file
    hass.http.register_view(TeslaPemView)
    
    # Register static path for optional UI
    integration_dir = Path(__file__).parent
    www_dir = integration_dir / "www"
    if www_dir.exists():
        hass.http.register_static_path(
            "/tesla_serve_key",
            str(www_dir),
            cache_headers=False
        )
        _LOGGER.info("Registered static path for Tesla Serve Key UI at /tesla_serve_key")
    
    _LOGGER.info("Tesla Serve Key integration set up successfully")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True


class TeslaPemView(HomeAssistantView):
    """View to serve the Tesla public key PEM file."""

    url = "/.well-known/appspecific/com.tesla.3p.public-key.pem"
    name = "api:tesla_serve_key:pem"
    requires_auth = False

    def _get_pem_file_path(self, hass: HomeAssistant) -> str | None:
        """Find the PEM file in the HA config directory.
        
        Checks in priority order:
        1. .well-known/appspecific/com.tesla.3p.public-key.pem
        2. tesla-public-key.pem
        """
        config_dir = Path(hass.config.config_dir)
        
        # Priority-ordered list of PEM file locations
        pem_locations = [
            config_dir / ".well-known" / "appspecific" / "com.tesla.3p.public-key.pem",
            config_dir / "tesla-public-key.pem",
        ]
        
        for pem_path in pem_locations:
            if pem_path.is_file():
                _LOGGER.debug("Found Tesla PEM file at: %s", pem_path)
                return str(pem_path)
        
        _LOGGER.error(
            "Tesla PEM file not found. Please place your Tesla public key at one of: %s",
            ", ".join(str(p) for p in pem_locations)
        )
        return None

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests for the PEM file."""
        hass = request.app["hass"]
        pem_path = self._get_pem_file_path(hass)
        
        if pem_path is None:
            return web.Response(
                text="PEM file not found. Please place the Tesla public key in the Home Assistant config directory.",
                status=404
            )
        
        try:
            # Read file on every request to ensure we serve the latest version
            with open(pem_path, "r") as f:
                pem_content = f.read()
            
            return web.Response(
                text=pem_content,
                content_type="application/x-pem-file",
                headers={
                    "Cache-Control": "public, max-age=86400"
                }
            )
        except Exception as e:
            _LOGGER.error("Error reading PEM file: %s", e)
            return web.Response(
                text="Error reading PEM file",
                status=500
            )

    async def head(self, request: web.Request) -> web.Response:
        """Handle HEAD requests for the PEM file."""
        hass = request.app["hass"]
        pem_path = self._get_pem_file_path(hass)
        
        if pem_path is None:
            return web.Response(status=404)
        
        try:
            # Check if file exists and get size
            file_size = os.path.getsize(pem_path)
            
            return web.Response(
                status=200,
                content_type="application/x-pem-file",
                headers={
                    "Cache-Control": "public, max-age=86400",
                    "Content-Length": str(file_size)
                }
            )
        except Exception as e:
            _LOGGER.error("Error checking PEM file: %s", e)
            return web.Response(status=500)