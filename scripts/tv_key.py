#!/usr/bin/env python3
"""Send one or more remote key presses to the paired Samsung TV.

Usage:  tv_key.py KEY_MENU
        tv_key.py KEY_LEFT KEY_LEFT KEY_ENTER
        tv_key.py --delay 0.6 KEY_DOWN KEY_DOWN KEY_ENTER

Keys are Samsung remote codes (KEY_HOME, KEY_MENU, KEY_UP/DOWN/LEFT/RIGHT, KEY_ENTER,
KEY_RETURN, KEY_EXIT, KEY_VOLUP, KEY_POWER, ...). This only emulates remote buttons; it
cannot read the screen. Collaborative driving: a human watches the TV and confirms.
"""
import sys, time, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKEN = str(ROOT / ".credentials" / "tv-token.txt")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between keys")
    ap.add_argument("--host", default="192.168.1.164")
    ap.add_argument("keys", nargs="+")
    a = ap.parse_args()

    from samsungtvws import SamsungTVWS
    tv = SamsungTVWS(host=a.host, port=8002, token_file=TOKEN,
                     name="Mac mini (TV Home setup)", timeout=15)
    for i, k in enumerate(a.keys):
        key = k if k.upper().startswith("KEY_") else "KEY_" + k.upper()
        tv.send_key(key)
        print(f"  sent {key}")
        if i < len(a.keys) - 1:
            time.sleep(a.delay)
    time.sleep(0.3)
    try:
        tv.close()
    except Exception:
        pass
    print("done")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"!! {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
