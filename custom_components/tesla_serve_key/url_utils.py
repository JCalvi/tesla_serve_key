"""URL helpers for Tesla Serve Key."""

from __future__ import annotations

import os

PEM_PATH = "/.well-known/appspecific/com.tesla.3p.public-key.pem"
PORT_OVERRIDE_ENV_VARS = ("TESLA_SERVE_KEY_PORT", "HASS_SERVER_PORT", "SUPERVISOR_PORT")


def _as_int_port(value) -> int | None:
    """Return validated port value or None."""
    try:
        port = int(value)
    except (TypeError, ValueError):
        return None
    if 1 <= port <= 65535:
        return port
    return None


def _get_runtime_port(hass) -> int | None:
    """Read HA runtime server port when available."""
    http_port = _as_int_port(getattr(getattr(hass, "http", None), "server_port", None))
    if http_port is not None:
        return http_port

    api_port = _as_int_port(getattr(getattr(getattr(hass, "config", None), "api", None), "port", None))
    if api_port is not None:
        return api_port

    return None


def _get_runtime_host(hass) -> str:
    """Read runtime host when available."""
    api = getattr(getattr(hass, "config", None), "api", None)
    return (
        getattr(api, "host", None)
        or getattr(api, "local_ip", None)
        or "localhost"
    )


def _get_runtime_scheme(hass) -> str:
    """Read runtime scheme when available."""
    api = getattr(getattr(hass, "config", None), "api", None)
    if getattr(api, "use_ssl", False):
        return "https"
    return "http"


def _build_url(scheme: str, host: str, port: int) -> str:
    """Build base URL and omit standard ports."""
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        return f"{scheme}://{host}"
    return f"{scheme}://{host}:{port}"


def resolve_base_url(hass, env: dict[str, str] | None = None) -> str:
    """Resolve Home Assistant base URL from configured URLs or runtime values."""
    config = getattr(hass, "config", None)
    external_url = getattr(config, "external_url", None)
    if external_url:
        return external_url.rstrip("/")

    internal_url = getattr(config, "internal_url", None)
    if internal_url:
        return internal_url.rstrip("/")

    if env is None:
        env = os.environ

    for var_name in PORT_OVERRIDE_ENV_VARS:
        override_port = _as_int_port(env.get(var_name))
        if override_port is not None:
            scheme = _get_runtime_scheme(hass)
            host = _get_runtime_host(hass)
            return _build_url(scheme, host, override_port)

    runtime_port = _get_runtime_port(hass)
    if runtime_port is None:
        scheme = _get_runtime_scheme(hass)
        runtime_port = 443 if scheme == "https" else 80
    else:
        scheme = _get_runtime_scheme(hass)

    host = _get_runtime_host(hass)
    return _build_url(scheme, host, runtime_port)


def resolve_pem_url(hass, env: dict[str, str] | None = None) -> str:
    """Resolve full PEM URL."""
    base_url = resolve_base_url(hass, env=env)
    return f"{base_url}{PEM_PATH}"
