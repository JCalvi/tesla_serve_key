# tesla_serve_key

Serve a Tesla public key from Home Assistant so it is available at:
`/.well-known/appspecific/com.tesla.3p.public-key.pem`

This repository contains a small helper to document how to serve your Tesla public key from Home Assistant by adding a tiny custom integration.

Source of instructions: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270)

## Installation HACS

1. Add this repo to HACS custom repositories.
2. Add your public key to `/config` with one of these filenames (checked in order):
   - `tesla-public-key.pem` (recommended)
   - `.tesla/tesla-public-key.pem` (in a hidden .tesla directory)
   - `tesla_fleet_public_key.pem` (alternative name)
3. Restart Home Assistant.

4. Verify your public key is being served by visiting:
   ```txt
   https://yourdomain.tld/.well-known/appspecific/com.tesla.3p.public-key.pem
   ```


## Installation (manual/custom integration)

Refer: [home-assistant/core issue #135116 comment](https://github.com/home-assistant/core/issues/135116#issuecomment-2609041270

That's it — this tiny custom integration registers a static path so Home Assistant will serve your Tesla public key file from one of the supported locations at the Tesla-specific well-known path.
