# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a Home Assistant custom integration that serves your Tesla Fleet API public key at the Tesla-required well-known path.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## Features

- ✅ Serves Tesla public key at the fixed well-known path required by Tesla Fleet API
- ✅ Unauthenticated endpoint (no authentication required)
- ✅ Automatically searches for PEM file in multiple locations
- ✅ Clear error logging if PEM file is not found
- ✅ No configuration required beyond placing the PEM file

## GitHub Pages Setup (For Repository Maintainers)

This repository uses GitHub Pages to serve documentation. To enable GitHub Pages deployment:

1. Navigate to the repository **Settings** > **Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Save the configuration

The workflow in `.github/workflows/deploy.yml` will automatically deploy the `index.html` file to GitHub Pages on every push to the `main` branch or when manually triggered.

Once configured, the documentation will be available at: `https://[username].github.io/tesla_serve_key/`

## Installation via HACS

1. Add this repository to HACS as a custom repository.
2. Install the "Tesla Serve Key" integration via HACS.
3. Place your Tesla Fleet API public key in the Home Assistant `/config` directory with one of these filenames (checked in priority order):
   - `tesla-public-key.pem` (recommended)
   - `tesla_fleet_public_key.pem`
   - `tesla-fleet-public-key.pem`
4. Add the integration to your `configuration.yaml`:
   ```yaml
   tesla_serve_key:
   ```
5. Restart Home Assistant.
6. Verify the key is served at:
   ```
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```

## Manual Installation

1. Open a file/text editor in Home Assistant (VS Code add-on recommended).
2. Navigate to the `/config` directory.
3. Place your Tesla Fleet API public key in `/config` with one of these filenames (checked in priority order):
   - `tesla-public-key.pem` (recommended)
   - `tesla_fleet_public_key.pem`
   - `tesla-fleet-public-key.pem`
4. Create a `custom_components` directory in `/config/` if it doesn't exist.
5. Download or copy the `tesla_serve_key` folder from this repository into `custom_components/`.
6. Add the integration to your `configuration.yaml`:
   ```yaml
   tesla_serve_key:
   ```
7. Restart Home Assistant.
8. Check the Home Assistant logs to confirm the integration loaded successfully.
9. Verify the key is served at:
   ```
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```
   Replace `yourdomain.tld` with your Home Assistant public URL.

## How It Works

This integration:
1. Searches for your Tesla public key in the Home Assistant config directory
2. Registers a static path handler that serves the file at `/.well-known/appspecific/com.tesla.3p.public-key.pem`
3. Ensures the endpoint is unauthenticated (accessible without Home Assistant authentication)

The integration does NOT include the PEM file - you must provide your own Tesla Fleet API public key.

## Troubleshooting

**Integration fails to load:**
- Check the Home Assistant logs for error messages
- Ensure the PEM file exists in one of the supported locations
- Verify the PEM file has the correct permissions (readable by Home Assistant)

**Key not accessible at well-known path:**
- Verify Home Assistant is accessible via HTTPS with a valid certificate
- Check that no other integration or configuration conflicts with the path
- Test accessing the URL from outside your local network if Tesla servers need to reach it

## Getting Your Tesla Fleet API Public Key

To obtain your Tesla Fleet API public key:
1. Follow Tesla's Fleet API documentation
2. Generate a public/private key pair for your application
3. Upload the public key to Tesla's Fleet API portal
4. Save the public key PEM file to your Home Assistant config directory

## Security

- The endpoint is intentionally **unauthenticated** as required by Tesla Fleet API
- Only the **public** key is served (never include your private key in Home Assistant)
- The well-known path is **fixed** and cannot be changed (Tesla Fleet API requirement)

## License

See [LICENSE](LICENSE) file for details.
