"""Tesla Serve Key integration for Home Assistant.

Serves the Tesla Fleet API public key at the well-known path.
"""
import logging
import os

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tesla_serve_key"

# Well-known path for Tesla Fleet API public key (fixed, cannot be changed)
WELL_KNOWN_PATH = "/.well-known/appspecific/com.tesla.3p.public-key.pem"

# PEM file locations to check (in priority order)
# The integration will use the first file that exists
PEM_FILE_LOCATIONS = [
    "/config/tesla-public-key.pem",
    "/config/tesla_fleet_public_key.pem",
    "/ssl/tesla-public-key.pem",
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Tesla Serve Key integration.
    
    This integration serves a Tesla Fleet API public key at the well-known path.
    The endpoint is unauthenticated (authentication hard-coded to False).
    """
    # Find the first PEM file that exists
    pem_file_path = None
    for file_path in PEM_FILE_LOCATIONS:
        if os.path.isfile(file_path):
            pem_file_path = file_path
            _LOGGER.info("Found Tesla public key at: %s", file_path)
            break
    
    if pem_file_path is None:
        _LOGGER.error(
            "No Tesla public key file found. Searched locations: %s",
            ", ".join(PEM_FILE_LOCATIONS)
        )
        return False
    
    # Register the static path with authentication disabled (hard-coded to False)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                WELL_KNOWN_PATH,
                pem_file_path,
                False,  # Authentication disabled (unauthenticated endpoint)
            )
        ]
    )
    
    _LOGGER.info(
        "Tesla Serve Key: Serving %s from %s (unauthenticated)",
        WELL_KNOWN_PATH,
        pem_file_path
    )
    
    return True