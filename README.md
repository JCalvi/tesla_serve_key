# Tesla Serve Key

A Home Assistant custom integration that serves your Tesla public key from the well-known path required by Tesla Fleet API:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This integration allows you to use Tesla Fleet API with Home Assistant by serving your public key from the correct path without requiring a separate web server.

**Important**: This integration does NOT include the Tesla public key PEM file. You must generate and place it yourself.

## Installation

### Option 1: HACS (Recommended)

1. Add this repository to HACS as a custom repository:
   - In HACS, go to Integrations
   - Click the three dots menu (⋮) in the top right
   - Select "Custom repositories"
   - Add URL: `https://github.com/JCalvi/tesla_serve_key`
   - Category: Integration
   - Click "Add"

2. Install the integration:
   - Find "Tesla Serve Key" in HACS
   - Click "Download"
   - Restart Home Assistant

3. Add the integration:
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "Tesla Serve Key"
   - Follow the setup wizard (you'll only need to provide a friendly name)

### Option 2: Manual Installation

1. Download this repository
2. Copy the `custom_components/tesla_serve_key` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add the integration via Settings → Devices & Services → Add Integration → Tesla Serve Key

## Setup

### 1. Generate Your Tesla Public/Private Key Pair

If you haven't already, generate your key pair:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out tesla-private-key.pem
openssl ec -in tesla-private-key.pem -pubout -out tesla-public-key.pem
```

**Security Warning**: Keep `tesla-private-key.pem` secure and private. Never commit it to version control or share it publicly.

### 2. Place the Public Key

Place your `tesla-public-key.pem` file in one of these locations in your Home Assistant config directory (checked in priority order):

1. `<config>/.well-known/appspecific/com.tesla.3p.public-key.pem` (recommended)
2. `<config>/tesla-public-key.pem`

**Example for location 1** (recommended):
```bash
mkdir -p /config/.well-known/appspecific/
cp tesla-public-key.pem /config/.well-known/appspecific/com.tesla.3p.public-key.pem
```

**Example for location 2**:
```bash
cp tesla-public-key.pem /config/tesla-public-key.pem
```

**Important**: Do NOT place the PEM file inside the `custom_components/tesla_serve_key` folder.

### 3. Restart Home Assistant

After placing the PEM file, restart Home Assistant for the changes to take effect.

## Verification

### Method 1: Using curl (recommended)

From any device that can reach your Home Assistant instance:

```bash
curl https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
```

You should see your public key content starting with:
```
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
```

### Method 2: Using the built-in UI

Navigate to: `https://yourdomain.tld/tesla_serve_key/`

This convenience page will:
- Display your public key
- Show where to place the PEM file
- Provide troubleshooting information
- Allow you to copy the key to clipboard

### Method 3: Using a web browser

Simply visit: `https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem`

You should see the PEM content displayed in your browser.

## Configuration

The integration uses a config flow and can be configured through the Home Assistant UI:
- **Name**: A friendly name for the integration (default: "Tesla Serve Key")
- The endpoint path (`/.well-known/appspecific/com.tesla.3p.public-key.pem`) is fixed and cannot be changed
- Authentication is disabled for this endpoint to allow Tesla servers to access it

## Security Notes

1. **Public Key Only**: This integration serves your PUBLIC key only. Never expose your private key.

2. **No Authentication**: The well-known path is intentionally served without authentication (`requires_auth = False`) because Tesla's servers need to access it.

3. **Safe to Expose**: The public key is safe to expose publicly - it cannot be used to impersonate you or access your Tesla account.

4. **Cache Control**: The PEM is served with `Cache-Control: public, max-age=86400` headers (24-hour cache) for optimal performance.

5. **File Not Included**: This repository intentionally does not include any PEM files. You must generate and manage your own keys.

## Troubleshooting

### Integration doesn't appear in UI

- Ensure you have restarted Home Assistant after installing the integration
- Check that `manifest.json` has `"config_flow": true`
- Check Home Assistant logs for any errors

### 404 Error when accessing the well-known path

- Verify the PEM file exists at one of the supported locations
- Check file permissions (Home Assistant must be able to read it)
- Check Home Assistant logs for error messages about PEM file location
- Ensure the integration is properly installed and enabled

### Key not found / File read errors

The integration reads the PEM file on every request. Check:
1. File exists at a supported location
2. File has correct permissions (readable by Home Assistant)
3. File path is correct (case-sensitive on Linux)
4. Check Home Assistant logs for specific error messages

### Key not updating

The integration reads the file from disk on every request, so updates should be immediate. If changes aren't reflected:
1. Verify you updated the file at the correct location
2. Clear your browser cache
3. Wait for the 24-hour cache to expire, or use `curl` with `--no-cache` header

## Version History

### 0.2.0
- Added config flow for UI-based installation
- Implemented HomeAssistantView with proper security settings
- Added optional convenience UI at `/tesla_serve_key/`
- Updated documentation with comprehensive setup and verification steps
- Changed to read PEM file from HA config directory on each request
- Support for two PEM file locations in priority order

### 0.1.0
- Initial release
- Basic static file serving

## Credits

Original instructions from: [home-assistant/core issue #135116](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## License

See LICENSE file for details.

