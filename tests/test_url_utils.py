"""Tests for runtime URL resolution."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

_MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "tesla_serve_key"
    / "url_utils.py"
)
_SPEC = importlib.util.spec_from_file_location("tesla_serve_key_url_utils", _MODULE_PATH)
assert _SPEC and _SPEC.loader
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
resolve_pem_url = _MODULE.resolve_pem_url


def _fake_hass(*, external_url=None, internal_url=None, server_port=None, api_port=None, use_ssl=False):
    api = SimpleNamespace(port=api_port, use_ssl=use_ssl, host="localhost")
    config = SimpleNamespace(external_url=external_url, internal_url=internal_url, api=api)
    http = SimpleNamespace(server_port=server_port)
    return SimpleNamespace(config=config, http=http)


class ResolvePemUrlTests(unittest.TestCase):
    """Validate HA URL/port handling."""

    def test_default_path_when_runtime_port_is_80(self):
        hass = _fake_hass(server_port=80)
        self.assertEqual(
            resolve_pem_url(hass),
            "http://localhost/.well-known/appspecific/com.tesla.3p.public-key.pem",
        )

    def test_explicit_custom_port_override(self):
        hass = _fake_hass(server_port=80)
        self.assertEqual(
            resolve_pem_url(hass, env={"TESLA_SERVE_KEY_PORT": "9443"}),
            "http://localhost:9443/.well-known/appspecific/com.tesla.3p.public-key.pem",
        )

    def test_non_8123_runtime_port_is_auto_detected(self):
        hass = _fake_hass(server_port=9000)
        self.assertEqual(
            resolve_pem_url(hass),
            "http://localhost:9000/.well-known/appspecific/com.tesla.3p.public-key.pem",
        )


if __name__ == "__main__":
    unittest.main()
