#!/usr/bin/env python3
"""Pair with the Samsung TV over its WebSocket remote API and snapshot a baseline.

First run pops an "Allow this device?" box on the TV; once allowed, the TV hands
back a token that is saved to .credentials/tv-token.txt so later runs are silent.
Then it records the installed-app list and device info as a timestamped baseline
under backups/ (Phase 0 of the debloat: back up before changing anything).

Nothing here changes a single TV setting. Read-only.
"""
import sys, os, json, ssl, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = os.environ.get("TV_HOST", "192.168.1.164")
CRED = ROOT / ".credentials"
BACK = ROOT / "backups"
CRED.mkdir(exist_ok=True)
BACK.mkdir(exist_ok=True)
TOKEN_FILE = CRED / "tv-token.txt"

from samsungtvws import SamsungTVWS

def main():
    first_time = not TOKEN_FILE.exists()
    if first_time:
        print(">> Connecting for the first time.")
        print(">> WATCH THE TV: an 'Allow this device?' box will appear.")
        print(">> Select Allow (highlight it and press the center/enter button).")
    else:
        print(">> Reusing saved token (no prompt expected).")

    tv = SamsungTVWS(
        host=HOST, port=8002,
        token_file=str(TOKEN_FILE),
        name="Mac mini (TV Home setup)",
        timeout=90,
    )

    # app_list() opens the authorized channel; first call triggers the Allow box.
    apps = tv.app_list()
    info = tv.rest_device_info()

    token_ok = TOKEN_FILE.exists() and TOKEN_FILE.read_text().strip()
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = {
        "captured_at": stamp,
        "host": HOST,
        "device_info": info,
        "installed_apps": apps,
    }
    out = BACK / f"baseline-apps-{stamp}.json"
    out.write_text(json.dumps(snap, indent=2))

    print("\n=== PAIRED" if token_ok else "\n=== CONNECTED (no token returned)")
    n = len(apps) if isinstance(apps, list) else 0
    print(f"=== installed apps reported: {n}")
    if isinstance(apps, list):
        for a in apps:
            print("   ", a.get("appId", "?"), "|", a.get("name", "?"),
                  "| running" if a.get("is_visible") or a.get("running") else "")
    print(f"\n=== baseline saved: {out}")
    print(f"=== token saved: {TOKEN_FILE} ({'yes' if token_ok else 'MISSING'})")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n!! {type(e).__name__}: {e}", file=sys.stderr)
        print("!! If the Allow box did not appear or you did not press it in time,"
              " just say so and I'll re-run; it will pop again.", file=sys.stderr)
        sys.exit(1)
