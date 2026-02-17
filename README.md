# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a Home Assistant custom integration that serves your Tesla Fleet public key from the well-known path required by Tesla. The integration reads the PEM file from your Home Assistant configuration directory (not from the integration folder) on every request.

**Important**: This integration does NOT include a PEM file. You must generate and place your own Tesla Fleet public key in your Home Assistant configuration directory.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## Installation

### Option 1: HACS (Recommended)

1. Add this repository to HACS as a custom repository:
   - Open HACS in Home Assistant
   - Go to Integrations
   - Click the three dots menu (top right) → Custom repositories
   - Add `https://github.com/JCalvi/tesla_serve_key` as an Integration
   - Click "Add"

2. Install the integration:
   - Search for "Tesla Serve Key" in HACS
   - Click "Download"
   - Restart Home Assistant

3. Place your Tesla Fleet public key in your Home Assistant configuration directory at one of these locations (in order of preference):
   ```
   <config>/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```
   or
   ```
   <config>/tesla-public-key.pem
   ```
   
   **Do NOT place the PEM file inside the `custom_components/tesla_serve_key` directory!**

4. Add the integration:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Tesla Serve Key"
   - Enter a friendly name (e.g., "Tesla Serve Key")
   - Click "Submit"

5. Verify the key is being served:
   ```bash
   curl -i https://YOUR_HA_URL/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```
   You should see:
   - HTTP 200 status
   - `Content-Type: application/x-pem-file` header
   - `Cache-Control: public, max-age=86400` header
   - Your PEM file contents in the response body

### Option 2: Manual Installation

1. Create the integration directory:
   ```bash
   mkdir -p /config/custom_components/tesla_serve_key
   ```

2. Download the integration files from this repository and place them in `/config/custom_components/tesla_serve_key/`:
   - `__init__.py`
   - `config_flow.py`
   - `manifest.json`
   - `www/index.html`

3. Place your Tesla Fleet public key in your Home Assistant configuration directory at one of these locations (in order of preference):
   ```
   /config/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```
   or
   ```
   /config/tesla-public-key.pem
   ```
   
   **Do NOT place the PEM file inside `/config/custom_components/tesla_serve_key/`!**

4. Restart Home Assistant

5. Add the integration:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Tesla Serve Key"
   - Enter a friendly name (e.g., "Tesla Serve Key")
   - Click "Submit"

6. Verify the key is being served:
   ```bash
   curl -i https://YOUR_HA_URL/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```

## Configuration

The integration is configured through the Home Assistant UI. The endpoint path (`/.well-known/appspecific/com.tesla.3p.public-key.pem`) and authentication (unauthenticated access) are fixed and cannot be changed.

When you add the integration, you only need to provide a friendly name for the config entry.

## How It Works

- The integration registers an HTTP endpoint at the fixed Tesla well-known path
- The endpoint is **unauthenticated** (`requires_auth = False`) so Tesla can access it
- On each request, the integration searches for your PEM file in these locations (in order):
  1. `<config>/.well-known/appspecific/com.tesla.3p.public-key.pem`
  2. `<config>/tesla-public-key.pem`
- If found, it serves the PEM with:
  - `Content-Type: application/x-pem-file`
  - `Cache-Control: public, max-age=86400`
- If not found, it returns HTTP 404 and logs an error message with the expected file locations
- Supports both GET and HEAD requests

## Viewing Your Key

After installation, you can view your served public key by visiting:
```
https://YOUR_HA_URL/tesla_serve_key/
```

This page displays the key and provides a "Copy to Clipboard" button.

## Troubleshooting

### HTTP 404 Not Found

If you get a 404 error, check the Home Assistant logs. The integration will log where it expects to find the PEM file. Make sure:
- The PEM file is in your Home Assistant config directory (usually `/config`)
- The filename is exactly `com.tesla.3p.public-key.pem` in a `.well-known/appspecific/` subdirectory, or `tesla-public-key.pem` in the config root
- The file has the correct permissions (readable by Home Assistant)

### Where is the config directory?

The default Home Assistant config directory is usually `/config` when running in Docker/Supervised, or `~/.homeassistant` when running in a virtual environment. You can find your config directory by:
- Looking at the Home Assistant log files on startup
- Using the File Editor add-on (it opens in the config directory by default)
- Checking Settings → System → Repairs (may show the path in some messages)

### Updating the PEM

Since the integration reads the PEM file on every request, you can update your public key by simply replacing the file. No restart of Home Assistant is required.

## GitHub Pages Setup (For Repository Maintainers)

This repository uses GitHub Pages to serve documentation. To enable GitHub Pages deployment:

1. Navigate to the repository **Settings** > **Pages**
2. Under **Build and deployment**, set **Source** to **GitHub Actions**
3. Save the configuration

The workflow in `.github/workflows/deploy.yml` will automatically deploy the `index.html` file to GitHub Pages on every push to the `main` branch or when manually triggered.

Once configured, the documentation will be available at: `https://[username].github.io/tesla_serve_key/`

