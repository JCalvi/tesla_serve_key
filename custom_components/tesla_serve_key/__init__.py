import logging
import os

from homeassistant.components.http import StaticPathConfig

DOMAIN = "tesla_serve_key"

_LOGGER = logging.getLogger(__name__)

# Priority-ordered list of possible PEM file locations
PEM_FILE_LOCATIONS = [
    "/config/tesla-public-key.pem",
    "/config/.tesla/tesla-public-key.pem",
    "/config/tesla_fleet_public_key.pem",
]


def find_pem_file():
    """Find the first existing PEM file from the list of possible locations."""
    for pem_path in PEM_FILE_LOCATIONS:
        if os.path.isfile(pem_path):
            _LOGGER.info("Found Tesla PEM file at: %s", pem_path)
            return pem_path
    
    _LOGGER.error(
        "Tesla PEM file not found in any of the expected locations: %s",
        ", ".join(PEM_FILE_LOCATIONS)
    )
    return None


async def async_setup(hass, config):
    """Set up the Tesla Serve Key integration."""
    pem_file_path = find_pem_file()
    
    if pem_file_path is None:
        _LOGGER.error(
            "Cannot set up Tesla Serve Key: PEM file not found. "
            "Please place your Tesla public key file in one of these locations: %s",
            ", ".join(PEM_FILE_LOCATIONS)
        )
        return False
    
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                "/.well-known/appspecific/com.tesla.3p.public-key.pem",
                pem_file_path,
                False,
            )
        ]
    )
    
    _LOGGER.info(
        "Tesla Serve Key integration set up successfully. "
        "Serving PEM from: /.well-known/appspecific/com.tesla.3p.public-key.pem"
    )
    
    return True