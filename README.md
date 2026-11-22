# PR 203 evidence (coffee_maker), synthetic only

Everything here is rendered from the card build at feat/eletta-explore-coffee-maker b12f0b0cd947b6c134e30e27054d0ee0847b6ae9 against invented states (`sensor.demo_duck_machine_status`). No Home Assistant connection, no real entity IDs, hostnames, or device data. Screenshots are re-encoded as plain RGB PNGs with no metadata.

- `coffee-maker-mobile-dark.png`, `-mobile-light.png` (390 px), `-narrow-dark.png` (320 px), `-desktop-dark.png`, `-desktop-light.png` (1200 px, 3 columns). The card surface is always dark by design; only the page theme changes.
- `espresso.png`: the new original espresso glyph (script: `reproducer/espresso-glyph.py`).
- `reproducer/`: `harness.html` + `run.py` load the built `appliance-card.js` in headless Chromium and check that every stage icon is a `data:image/png` URI that actually decodes (`naturalWidth` 1024), that no request leaves localhost, and that labels stay clear of the machine image. Result: `browser-result.json`. Build with `npm ci && npm run build`, copy `appliance-card.js` next to `harness.html`, then `uv run --with playwright python run.py`.
