# Samsung Q70T Debloat (reversible)

TV: Samsung QN82Q70TAFXZA (82" Q70T, 2020, US), Tizen 5.5, at 192.168.1.164.
Baseline snapshot: `backups/baseline-20261022-181431.json` (paired token + device info).

These are all changes made through the TV's own Settings, by hand on the remote. Nothing
here is scripted: Samsung's public API exposes app-launch and key-press, not settings
read/write, and the set is not rooted, so there is no programmatic way to set or read these.
Every item except **Reset PSID** is reversible from the same screen; see `restore.md`.

Tailored to Max's choices (2026-10-22): keep remote voice ON (used inside YouTube); kill
Samsung TV Plus; reset the advertising ID; protect Netflix, YouTube, Disney+, Prime Video,
HBO Max, Twitch, Hulu.

Path caveat: 2020 firmware labels vary slightly and the **Terms & Privacy** location is the
least certain (it may sit under Settings > Support, or be reached from Home > far-left menu >
Privacy Choices). If what you see differs from a path below, tell me what is on screen and I
will adjust.

## Group 1. Privacy, ads, viewing data
Open: **Settings > Support > Terms & Privacy** (or **Home**, move **Left** to the far-left
Home menu > **Privacy Choices**).
1. **Viewing Information Services (ACR)** -> **Disagree / untick.** The big one: stops the TV
   fingerprinting what is on screen and sending viewing history. No functional loss.
2. **Interest-Based Advertisements** -> **Disagree / untick.** Stops ad targeting. Ads still
   appear (Samsung does not let you remove them), just untargeted.
3. **Reset PSID** -> **activate.** Fresh advertising ID so old data is not reused. ONE-WAY.
   - **Leave Voice Recognition Services ON** (turning it off can break YouTube voice search).
   - **Leave Smart Hub Terms / Privacy Notice alone** (the only way to decline is a Smart Hub
     reset, which wipes apps and logins).

## Group 2. Remote support
4. **Settings > Support > Remote Management -> Off.** Stops Samsung opening a remote session.
   Firmware updates are a separate setting and keep working.

## Group 3. Voice extras (push-to-talk for YouTube stays working)
5. **Settings > General > Voice > Voice Hint -> Off** (hides command pop-ups).
6. **Settings > General > Voice > Bixby Voice settings > Privacy -> Off** (less Bixby data).
7. **Voice Wake-up -> Off** if present (Bixby **Explore Now > Settings > Voice Wake-up**).
   Stops the always-listening "Hi Bixby"; push-and-hold voice (what YouTube uses) still works.

## Group 4. Auto-run / boot (less junk at power-on)
Open: **Settings > General > Smart Features.**
8. **Autorun Smart Hub -> Off.**
9. **Autorun Last App -> Off.** (We will revisit this if we add a custom dashboard later.)
10. **Autorun Samsung TV Plus -> Off** if this firmware shows it.

## Group 5. Samsung TV Plus (you said you never use it)
11. Home bar: highlight **Samsung TV Plus**, **press and hold Select** (or press **Down** on
    2020-21), choose **Remove**, then **Disable**. App cannot be uninstalled; this dormants it.
12. Optional: **Live TV > Channel List > Edit Channels >** select TV Plus channels **> Delete**
    to clear them from the guide.

## Group 6. Home bar cleanup (keep your apps)
13. For each tile you do NOT use: highlight it, **hold Select > Remove** (takes it off the bar,
    does NOT uninstall). KEEP: Netflix, YouTube, Disney+, Prime Video, HBO Max, Twitch, Hulu.
    Re-add later via **Apps > Settings (gear) > app > Add to Home**.

## Group 7. Notifications (optional)
14. **Home > far-left Home menu > Notification > Settings** -> untick services you do not want
    pop-ups from.

## Group 8. Pairing convenience (for our ongoing work)
15. **Settings > General > External Device Manager > Device Connect Manager > Access
    Notification -> First Time Only.** Stops the Allow box reappearing for this Mac every time.

## Speed, after the toggles (no setting risk)
- Cold boot: hold the remote **Power** button ~5 s until it restarts (clears cache). A normal
  off is only standby.
- **Settings > Support > Device Care > Start Device Care** (clears memory, closes stale apps).

## Left ALONE on purpose
- Smart Hub Terms / Privacy Notice (declining needs a destructive reset).
- Software Auto Update (keep on: security and bug fixes, not telemetry).
- Usage Mode = Home (never Retail).
- Samsung Account (stays signed in so you can still install apps).
- Power On with Mobile / IP Remote (kept on so our network tools can wake the TV).
- Never: Reset Smart Hub, Factory Reset, Reset Network, deleting apps (all destructive).

## What this does NOT stop
Samsung's first-screen Home-bar ad placements still appear (only untargeted); Samsung says
users cannot switch the ads off. Router/TV DNS blocking removes some of what is left and is an
optional follow-on (it carries its own risk of breaking the app store or updates, so it is
separate from this checklist).
