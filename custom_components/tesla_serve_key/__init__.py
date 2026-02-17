"""Tesla Serve Key integration - read PEM from Home Assistant config directory and serve at the Tesla well-known path."""

from pathlib import Path
import logging
from typing import Optional

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "tesla_serve_key"
# Fixed, non-configurable Tesla expected path served to clients
API_SERVE_PATH = "/.well-known/appspecific/com.tesla.3p.public-key.pem"

# Candidate locations (relative to Home Assistant config directory)
CANDIDATE_REL_PATHS = [
    ".well-known/appspecific/com.tesla.3p.public-key.pem",
    "tesla-public-key.pem",
]


def _find_pem_path(hass: HomeAssistant) -> Optional[Path]:
    """Find the PEM file in the Home Assistant config directory.

    Returns the first existing Path or None.
    """
    config_dir = Path(hass.config.path())
    for rel in CANDIDATE_REL_PATHS:
        candidate = config_dir / rel
        if candidate.exists():
            return candidate
    return None


def _make_view_class(entry_id: str, url: str) -> type:
    """Create a HomeAssistantView subclass for the entry with fixed url."""

    class_name = f"TeslaKeyView_{entry_id}"

    async def get(self, request):
        pem_path = _find_pem_path(request.app["hass"])
        if not pem_path:
            _LOGGER.error(
                "Tesla public key not found. Place the PEM at one of: %s",
                ", ".join(CANDIDATE_REL_PATHS),
            )
            return web.Response(status=404, text="Public key not found")
        try:
            text = pem_path.read_text(encoding="utf-8")
        except Exception as exc:
            _LOGGER.exception("Failed to read PEM file %s: %s", pem_path, exc)
            return web.Response(status=500, text="Failed to read public key")
        headers = {
            "Content-Type": "application/x-pem-file",
            "Cache-Control": "public, max-age=86400",
        }
        return web.Response(text=text, headers=headers)

    async def head(self, request):
        pem_path = _find_pem_path(request.app["hass"])
        if not pem_path:
            return web.Response(status=404, text="")
        headers = {
            "Content-Type": "application/x-pem-file",
            "Cache-Control": "public, max-age=86400",
        }
        return web.Response(status=200, text="", headers=headers)

    attrs = {
        "url": url,
        "name": f"api:{DOMAIN}:public_key:{entry_id}",
        # Authentication is intentionally fixed to False and is NOT exposed
        "requires_auth": False,
        "get": get,
        "head": head,
    }
    return type(class_name, (HomeAssistantView,), attrs)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration (no-op; config via config entries)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry.

    The endpoint path is fixed to API_SERVE_PATH and the PEM is looked-up
    in the Home Assistant config directory (not in the integration folder).
    """
    hass.data.setdefault(DOMAIN, {})

    view_cls = _make_view_class(entry.entry_id, API_SERVE_PATH)
    hass.http.register_view(view_cls)
    _LOGGER.debug("Registered Tesla Serve Key view at %s", API_SERVE_PATH)

    # static UI path (optional) served from integration www folder
    www_path = Path(__file__).parent / "www"
    hass.http.register_static_path(f"/{DOMAIN}", str(www_path), False)
    _LOGGER.debug("Registered static path /%s -> %s", DOMAIN, www_path)

    hass.data[DOMAIN][entry.entry_id] = {
        "entry": entry,
        "api_path": API_SERVE_PATH,
        "view_name": view_cls.name,
    }

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if DOMAIN not in hass.data or entry.entry_id not in hass.data[DOMAIN]:
        return True

    hass.data[DOMAIN].pop(entry.entry_id)
    # Proper unregister isn't provided by HA; a restart will remove routes.
    return True