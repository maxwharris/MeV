# MeV

A minimal, typographic home screen for a Samsung Tizen TV, a quiet launcher that
replaces the stock smart-TV home with a mostly-white, Times New Roman interface:
a clock, local weather, a short rotating line, columns of favourite apps, an HDMI
source switcher, an AirPlay how-to, and an idle screensaver that draws a slowly
rotating wireframe surface.

It is a sideloaded Tizen web app (`.wgt`). The UI is authored in
`work/mockups/index-app.html` with modern CSS, then transformed for the TV's
2019-era Chromium 69 engine by `scripts/build-tv.py` (it inlines the fonts and
rewrites CSS the old engine cannot parse) into `tizen/MaxHome/`.

## Layout

- `tizen/MaxHome/` — the Tizen app: `config.xml`, the generated `index.html`,
  `service/service.js` (a small background watchdog that returns to the launcher
  after an app exits), the bundled fonts and icon.
- `scripts/build-tv.py` — builds the TV `index.html` from the source page.
- `scripts/tv_key.py`, `scripts/tv_pair_and_backup.py` — pair with the TV over
  the local network and drive the remote during setup.
- `work/mockups/index-app.html` — the source UI (full-fat modern CSS).
- `docs/` — notes on reversibly turning off the stock TV's ads and telemetry.

## Notes

Fonts are Tinos (a Times New Roman metric clone) and Cousine (a Courier clone),
both open-licensed. Weather uses open, keyless endpoints. No accounts, no
telemetry, fully local.
