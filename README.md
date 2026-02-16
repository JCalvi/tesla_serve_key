# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a small helper to document how to serve your Tesla public key from Home Assistant by adding a tiny custom integration.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## Installation (manual/custom integration)

1. Open a file/text editor in Home Assistant (the VS Code add-on is recommended).
2. Navigate to the `/config` directory (default working directory for the VS Code add-on).
3. Add your public key to `/config` with the filename:
   ```
   tesla-public-key.pem
   ```
4. Create a `custom_components` directory in `/config/` if it doesn't already exist.
5. Create a directory `custom_components/tesla_serve_key/`.
6. Add the following files into `custom_components/tesla_serve_key/`:

   - `__init__.py`
   ```python
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
   ```

   - `manifest.json`
   ```json
   {
     "domain": "tesla_serve_key",
     "name": "Tesla Serve Key",
     "version": "0.1.0"
   }
   ```

7. Open your `configuration.yaml` and add the integration entry:
   ```yaml
   tesla_serve_key:
   ```

8. Restart Home Assistant.

9. Verify your public key is being served by visiting:
   ```txt
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```
   Replace `yourdomain.tld` with your Home Assistant public URL.

That's it — this tiny custom integration registers a static path so Home Assistant will serve the `tesla-public-key.pem` file from `/config` at the Tesla-specific well-known path.
