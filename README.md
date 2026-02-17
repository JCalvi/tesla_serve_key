# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a small helper to document how to serve your Tesla public key from Home Assistant by adding a tiny custom integration.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## Version 0.2.0 Features

- **Multiple file location support**: The integration automatically searches for your Tesla public key in multiple locations (in order of priority):
  1. `/config/tesla-public-key.pem`
  2. `/config/tesla_fleet_public_key.pem`
  3. `/ssl/tesla-public-key.pem`
- **Unauthenticated endpoint**: Authentication is hard-coded to disabled for the well-known path
- **Fixed path**: The well-known path `/.well-known/appspecific/com.tesla.3p.public-key.pem` cannot be changed
- **Logging**: The integration logs which PEM file it finds and serves

## GitHub Pages Setup (For Repository Maintainers)

This repository uses GitHub Pages to serve documentation. To enable GitHub Pages deployment:

1. Navigate to the repository **Settings** > **Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Save the configuration

The workflow in `.github/workflows/deploy.yml` will automatically deploy the `index.html` file to GitHub Pages on every push to the `main` branch or when manually triggered.

Once configured, the documentation will be available at: `https://[username].github.io/tesla_serve_key/`

## Installation HACS

1. Add this repo to HACS custom repositories.
2. Add your public key to one of the supported locations (the integration will use the first file it finds):
   - `/config/tesla-public-key.pem` (recommended)
   - `/config/tesla_fleet_public_key.pem`
   - `/ssl/tesla-public-key.pem`
3. Open your `configuration.yaml` and add the integration entry:
   ```yaml
   tesla_serve_key:
   ```
4. Restart Home Assistant.

5. Check the Home Assistant logs to verify which PEM file was found and is being served.

6. Verify your public key is being served by visiting:
   ```txt
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```


## Installation (manual/custom integration)

1. Open a file/text editor in Home Assistant (the VS Code add-on is recommended).
2. Navigate to the `/config` directory (default working directory for the VS Code add-on).
3. Add your public key to one of the supported locations (the integration will use the first file it finds):
   - `/config/tesla-public-key.pem` (recommended)
   - `/config/tesla_fleet_public_key.pem`
   - `/ssl/tesla-public-key.pem`
4. Create a `custom_components` directory in `/config/` if it doesn't already exist.
5. Create a directory `custom_components/tesla_serve_key/`.
6. Add the following files into `custom_components/tesla_serve_key/`:

   - `__init__.py`
   ```python
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
   ```

   - `manifest.json`
   ```json
   {
     "domain": "tesla_serve_key",
     "name": "Tesla Serve Key",
     "documentation": "https://github.com/JCalvi/tesla_serve_key",
     "codeowners": ["@JCalvi"],
     "requirements": [],
     "version": "0.2.0",
     "iot_class": "local_push"
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
