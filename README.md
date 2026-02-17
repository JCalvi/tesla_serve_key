# Tesla Serve Key - Home Assistant Integration

A Home Assistant custom integration that serves your Tesla public key at the required well-known path for Tesla API third-party integrations.

## Features

- ✅ Serves PEM file at `/.well-known/appspecific/com.tesla.3p.public-key.pem`
- ✅ Easy verification through Home Assistant UI
- ✅ Automatic file discovery from config directory
- ✅ No authentication required for the endpoint (as per Tesla requirements)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/JCalvi/ha-tesla-key-server` as an Integration
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/tesla_serve_key` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Setup

### 1. Generate Your Tesla Keys

Follow Tesla's documentation to generate your public/private key pair for third-party API access.

### 2. Place Your PEM File

Place your Tesla public key PEM file in one of these locations:

- **Recommended:** `<config>/.well-known/appspecific/com.tesla.3p.public-key.pem`
- **Alternative:** `<config>/tesla-public-key.pem`

Where `<config>` is your Home Assistant configuration directory (usually `/config`).

### 3. Add the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Tesla Serve Key**
4. Click to add it
5. Enter a friendly name (default: "Tesla Serve Key")
6. Click **Submit**

## Verify PEM is Being Served

### Method 1: Home Assistant UI

1. Go to **Settings** → **Devices & Services**
2. Find **Tesla Serve Key** integration
3. Click the **⚙️ Configure** button
4. A notification will appear showing:
   - ✅ Local file status
   - ✅ HTTP verification results
   - ✅ PEM file preview

### Method 2: Manual Check

Visit: `http://your-home-assistant-url/.well-known/appspecific/com.tesla.3p.public-key.pem`

You should see your PEM file content (starts with `-----BEGIN PUBLIC KEY-----`)

### Method 3: Optional Web UI

Visit: `http://your-home-assistant-url/tesla_serve_key/`

A simple verification page is available (if the `www` directory exists).

## Configuration

No additional configuration is required. The integration will:

1. Automatically detect your PEM file location
2. Serve it at the required Tesla endpoint
3. Handle all HTTP requests without authentication

## Troubleshooting

### PEM File Not Found

**Error:** `PEM file not found`

**Solution:** Ensure your PEM file is placed at one of the supported locations:
- `<config>/.well-known/appspecific/com.tesla.3p.public-key.pem`
- `<config>/tesla-public-key.pem`

### 404 Error When Accessing URL

**Issue:** Cannot access `/.well-known/appspecific/com.tesla.3p.public-key.pem`

**Solutions:**
1. Restart Home Assistant after placing the PEM file
2. Check that the integration is installed and loaded
3. Verify the PEM file exists using the verification feature
4. Check Home Assistant logs for errors

### PEM Verification Shows "Invalid Format"

**Issue:** File exists but shows invalid PEM format

**Solution:** Ensure your PEM file:
- Starts with `-----BEGIN PUBLIC KEY-----`
- Ends with `-----END PUBLIC KEY-----`
- Is a valid public key file (not a private key or certificate)

## File Structure

```
custom_components/tesla_serve_key/
├── __init__.py           # Main integration logic
├── config_flow.py        # Configuration and options flow
├── manifest.json         # Integration metadata
├── strings.json          # UI translations
└── www/                  # Optional web UI
    └── index.html        # Verification page
```

## Technical Details

### Endpoint Details

- **URL:** `/.well-known/appspecific/com.tesla.3p.public-key.pem`
- **Method:** GET
- **Authentication:** None required
- **Content-Type:** `application/x-pem-file`
- **Cache:** 24 hours

### Security Considerations

- The endpoint does NOT require authentication (as per Tesla's requirements)
- Only serves the PUBLIC key (never expose your private key)
- File is read on every request to ensure latest version is served
- Endpoint is read-only

## Support

If you encounter issues:

1. Check the Home Assistant logs
2. Use the built-in verification feature
3. Open an issue on GitHub: https://github.com/JCalvi/ha-tesla-key-server/issues

## License

MIT License - See LICENSE file for details

## Credits

Developed for the Home Assistant community to simplify Tesla third-party API integration.
