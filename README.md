# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a small helper to document how to serve your Tesla public key from Home Assistant by adding a tiny custom integration.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## GitHub Pages Setup (For Repository Maintainers)

This repository uses GitHub Pages to serve documentation. To enable GitHub Pages deployment:

1. Navigate to the repository **Settings** > **Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Save the configuration

The workflow in `.github/workflows/deploy.yml` will automatically deploy the `index.html` file to GitHub Pages on every push to the `main` branch or when manually triggered.

Once configured, the documentation will be available at: `https://[username].github.io/tesla_serve_key/`

## Installation HACS

1. Add this repo to HACS custom repositories.
2. Add your public key to `/config` with one of these filenames (checked in order):
   - `tesla-public-key.pem` (recommended)
   - `.tesla/tesla-public-key.pem` (in a hidden .tesla directory)
   - `tesla_fleet_public_key.pem` (alternative name)
3. Open your `configuration.yaml` and add the integration entry:
   ```yaml
   tesla_serve_key:
   ```
4. Restart Home Assistant.

5. Verify your public key is being served by visiting:
   ```txt
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```


## Installation (manual/custom integration)

1. Open a file/text editor in Home Assistant (the VS Code add-on is recommended).
2. Navigate to the `/config` directory (default working directory for the VS Code add-on).
3. Add your public key to `/config` with one of these filenames (checked in order):
   - `tesla-public-key.pem` (recommended)
   - `.tesla/tesla-public-key.pem` (in a hidden .tesla directory)
   - `tesla_fleet_public_key.pem` (alternative name)
4. Create a `custom_components` directory in `/config/` if it doesn't already exist.
5. Create a directory `custom_components/tesla_serve_key/`.
6. Add the following files into `custom_components/tesla_serve_key/`:

   - `__init__.py`
   ```python
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
   ```

   - `manifest.json`
   ```json
   {
     "domain": "tesla_serve_key",
     "name": "Tesla Serve Key",
     "version": "0.2.0"
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

That's it — this tiny custom integration registers a static path so Home Assistant will serve your Tesla public key file from one of the supported locations at the Tesla-specific well-known path.
