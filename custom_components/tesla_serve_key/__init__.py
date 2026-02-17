"""Tesla Serve Key integration for Home Assistant.

This integration serves the Tesla Fleet public key at the fixed well-known path.
"""
import logging
import os

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tesla_serve_key"

# Fixed well-known path for Tesla Fleet API
WELL_KNOWN_PATH = "/.well-known/appspecific/com.tesla.3p.public-key.pem"

# Priority-ordered list of PEM file locations in HA config directory
PEM_FILE_LOCATIONS = [
    "tesla-public-key.pem",
    "tesla_fleet_public_key.pem",
    "tesla-fleet-public-key.pem",
]


def find_pem_file(hass: HomeAssistant) -> str | None:
    """Find the PEM file in the HA config directory.
    
    Searches for the PEM file in priority order and returns the first one found.
    
    Args:
        hass: Home Assistant instance
        
    Returns:
        Full path to the PEM file if found, None otherwise
    """
    config_dir = hass.config.path()
    
    for filename in PEM_FILE_LOCATIONS:
        filepath = os.path.join(config_dir, filename)
        if os.path.isfile(filepath):
            _LOGGER.info("Found Tesla public key at: %s", filepath)
            return filepath
    
    return None


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Tesla Serve Key integration.
    
    This integration serves the Tesla Fleet public key at a fixed well-known path
    with authentication disabled (unauthenticated endpoint).
    
    Args:
        hass: Home Assistant instance
        config: Integration configuration
        
    Returns:
        True if setup was successful, False otherwise
    """
    pem_path = find_pem_file(hass)
    
    if pem_path is None:
        _LOGGER.error(
            "Tesla public key file not found. Please place the file in your "
            "Home Assistant config directory with one of these names: %s",
            ", ".join(PEM_FILE_LOCATIONS)
        )
        return False
    
    # Register the static path with authentication disabled (third parameter is False)
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                WELL_KNOWN_PATH,
                pem_path,
                False,  # Authentication disabled - this is an unauthenticated endpoint
            )
        ]
    )
    
    _LOGGER.info(
        "Tesla Serve Key integration loaded successfully. "
        "Public key is being served at: %s",
        WELL_KNOWN_PATH
    )
    
    return True