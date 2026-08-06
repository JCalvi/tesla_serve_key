# Tesla Serve Key
A custom integration for Home Assistant that serves a Tesla Fleet API public key from the required well-known HTTPS endpoint:
```text
/.well-known/appspecific/com.tesla.3p.public-key.pem
```
Tesla requires the public key to remain accessible at this endpoint on the application domain used for Fleet API registration.
## Features
- Serves the Tesla public key without Home Assistant authentication
- Supports the well-known endpoint required by Tesla Fleet API
- Automatically discovers the public key in the Home Assistant configuration directory
- Provides built-in file and HTTP verification
- Includes an optional browser-based verification page
- Uses Home Assistant's configured URLs and runtime HTTP port for verification
- Supports Home Assistant OS installations, including Home Assistant running on port `80`
- Reads the public key from disk for every request
## Requirements
- Home Assistant 2023.1.0 or later
- HACS for the recommended installation method
- A Tesla-compatible public/private key pair
- An HTTPS application domain that reaches your Home Assistant instance
Only the **public key** should be stored in Home Assistant. Keep the private key secure and never place it in a publicly served directory.
## Installation
### HACS — Recommended
[![Open your Home Assistant instance and add this repository to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=JCalvi&repository=tesla_serve_key&category=integration)
Alternatively, add the repository manually:
1. Open **HACS** in Home Assistant.
2. Select **Integrations**.
3. Open the three-dot menu in the top-right corner.
4. Select **Custom repositories**.
5. Enter:
   ```text
   https://github.com/JCalvi/tesla_serve_key
   ```
6. Select **Integration** as the repository type.
7. Select **Add**.
8. Find **Tesla Serve Key** in HACS.
9. Select **Download**.
10. Restart Home Assistant.
### Manual Installation
1. Download `tesla_serve_key.zip` from the latest [GitHub release](https://github.com/JCalvi/tesla_serve_key/releases).
2. Create the following directory in your Home Assistant configuration:
   ```text
   /config/custom_components/tesla_serve_key
   ```
3. Extract the **contents** of `tesla_serve_key.zip` directly into that directory.
4. Confirm that the manifest is located at:
   ```text
   /config/custom_components/tesla_serve_key/manifest.json
   ```
5. Restart Home Assistant.
The installed structure should resemble:
```text
/config/custom_components/tesla_serve_key/
├── __init__.py
├── config_flow.py
├── manifest.json
├── url_utils.py
└── www/
    └── index.html
```
## Tesla Key Preparation
Tesla requires a PEM-encoded EC public key using the `prime256v1` curve.
Tesla's instructions for generating and registering a virtual key are available in the [Tesla Fleet API Virtual Keys guide](https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide).
The public key should begin and end with:
```text
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
```
Do not use a private key or certificate in place of the public key.
## Public Key Location
Place the Tesla public key in one of the following locations.
### Recommended location
```text
/config/.well-known/appspecific/com.tesla.3p.public-key.pem
```
### Alternative location
```text
/config/tesla-public-key.pem
```
The recommended location takes priority when both files exist.
## Add the Integration
After installing the files and restarting Home Assistant:
1. Go to **Settings → Devices & Services**.
2. Select **Add Integration**.
3. Search for **Tesla Serve Key**.
4. Select the integration.
5. Enter a friendly name or retain the default.
6. Select **Submit**.
No YAML configuration is required.
## Public Endpoint
Once the integration is loaded, the public key is served at:
```text
https://<your-app-domain>/.well-known/appspecific/com.tesla.3p.public-key.pem
```
The application domain must match the domain used for your Tesla Fleet API application and partner registration.
The integration serves this endpoint without authentication, as required by Tesla.
The integration does not configure:
- DNS
- HTTPS certificates
- Home Assistant Cloud
- Reverse proxies
- Router port forwarding
- Tesla Fleet API registration
Your Home Assistant instance must already be publicly reachable through the application domain.
## Verification
### Home Assistant Verification
1. Go to **Settings → Devices & Services**.
2. Find **Tesla Serve Key**.
3. Select **Configure**.
4. Review the persistent notification created by the integration.
The notification reports:
- Whether the public key file was found
- The file location
- The URL used for HTTP verification
- The HTTP response status
- Whether the response resembles a public-key PEM file
- A short preview of the returned public key
For its built-in HTTP check, the integration uses the following URL priority:
1. Home Assistant external URL
2. Home Assistant internal URL
3. Home Assistant runtime host and HTTP port
### Direct Browser Check
Open:
```text
https://<your-app-domain>/.well-known/appspecific/com.tesla.3p.public-key.pem
```
A successful response should contain the public key beginning with:
```text
-----BEGIN PUBLIC KEY-----
```
### Verification Page
The integration also provides a browser-based verification page at:
```text
https://<your-home-assistant-url>/tesla_serve_key/
```
The page automatically checks the public-key endpoint and displays the result.
## Technical Details
### Public-Key Endpoint
| Property | Value |
|---|---|
| Path | `/.well-known/appspecific/com.tesla.3p.public-key.pem` |
| Method | `GET` |
| Home Assistant authentication | Not required |
| Content type | `application/x-pem-file` |
| Cache control | `public, max-age=86400` |
| File loading | Read from disk for every request |
### Security
- Only the public key should be served.
- The private key must remain secret.
- The endpoint is read-only.
- No Home Assistant access token is required for the endpoint.
- The integration does not expose other files from the Home Assistant configuration directory.
- The optional verification page displays only a limited preview of the public key.
## Updating
Updates are published through [GitHub Releases](https://github.com/JCalvi/tesla_serve_key/releases) and distributed through HACS.
When HACS reports that an update is available:
1. Open the update in Home Assistant or HACS.
2. Install the latest release.
3. Restart Home Assistant.
## Troubleshooting
### Integration Does Not Appear
After downloading the integration through HACS:
1. Restart Home Assistant.
2. Refresh the browser.
3. Go to **Settings → Devices & Services → Add Integration**.
4. Search for **Tesla Serve Key** again.
### Public Key Not Found
Confirm that the public key exists at one of these locations:
```text
/config/.well-known/appspecific/com.tesla.3p.public-key.pem
```
or:
```text
/config/tesla-public-key.pem
```
File and directory names are case-sensitive.
### Endpoint Returns 404
Check that:
- Tesla Serve Key has been added under **Devices & Services**
- Home Assistant was restarted after installation
- The public key exists at a supported location
- The integration loaded successfully
- Home Assistant logs do not show a Tesla Serve Key setup error
### Invalid PEM Format
Confirm that the file:
- Is the public key, not the private key
- Begins with `-----BEGIN PUBLIC KEY-----`
- Ends with `-----END PUBLIC KEY-----`
- Uses a Tesla-compatible `prime256v1` public key
- Does not contain unrelated text before or after the PEM data
### Local Verification Works but Tesla Cannot Access It
Confirm that:
- The endpoint is publicly available over HTTPS
- The public hostname matches the application domain registered with Tesla
- The HTTPS certificate is valid
- The endpoint can be opened without signing in to Home Assistant
- A reverse proxy or security service is not blocking `/.well-known/` requests
Test the endpoint from outside your local network rather than only through the local Home Assistant address.
## Support
Before reporting an issue:
1. Check the Home Assistant logs.
2. Run the integration's built-in verification.
3. Test the public endpoint in a browser.
4. Record the Home Assistant version and Tesla Serve Key version.
Issues can be reported through the [Tesla Serve Key issue tracker](https://github.com/JCalvi/tesla_serve_key/issues).
## Releases
Release history and downloadable packages are available on the [GitHub Releases page](https://github.com/JCalvi/tesla_serve_key/releases).
## License
Tesla Serve Key is released under the [MIT License](LICENSE).
