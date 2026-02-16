from homeassistant.components.http import StaticPathConfig

DOMAIN = "tesla_serve_key"


async def async_setup(hass, config):
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                "/.well-known/appspecific/com.tesla.3p.public-key.pem",
                "/config/tesla-public-key.pem",
                False,
            )
        ]
    )
    return True