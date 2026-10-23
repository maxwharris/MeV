# Restore: put the Samsung Q70T back the way it was

This is a guide, not an executable script, and that is a platform limit, not a shortcut:
Samsung's public API on this TV exposes app-launch and key-press only, not settings
read/write, and the set is not rooted, so nothing can write these values back automatically.
Each step below is the exact reverse of a change in `debloat.md`, done on the remote. (If we
later add router-level DNS blocking, that part IS scriptable and gets a real revert script.)

To undo everything, set each item back to the value in the right-hand column.

| # | Setting | Path to reach it | Set back to |
|---|---------|------------------|-------------|
| 1 | Viewing Information Services (ACR) | Settings > Support > Terms & Privacy (or Home > far-left > Privacy Choices) | **Agree / ticked** |
| 2 | Interest-Based Advertisements | same screen | **Agree / ticked** |
| 3 | Reset PSID | n/a | **Cannot be undone** (a new random ad ID replaced the old one; nothing was lost but the old ID is gone) |
| 4 | Remote Management | Settings > Support > Remote Management | **On** |
| 5 | Voice Hint | Settings > General > Voice > Voice Hint | **On** |
| 6 | Bixby use of personal information | Settings > General > Voice > Bixby Voice settings > Privacy | **On** |
| 7 | Voice Wake-up | Bixby Explore Now > Settings > Voice Wake-up | **On** |
| 8 | Autorun Smart Hub | Settings > General > Smart Features | **On** |
| 9 | Autorun Last App | Settings > General > Smart Features | **On** |
| 10 | Autorun Samsung TV Plus | Settings > General > Smart Features | **On** |
| 11 | Samsung TV Plus tile | Source > highlight Samsung TV Plus > press **Up** > Add to Home | re-added to Home bar |
| 12 | Deleted TV Plus channels | Live TV > Channel List > Edit Channels > select > **Restore** | restored |
| 13 | Removed Home-bar tiles | Apps > Settings (gear) > select app > **Add to Home** | re-added |
| 14 | Notification categories | Home > far-left > Notification > Settings | ticked |
| 15 | Device Connect Manager > Access Notification | Settings > General > External Device Manager > Device Connect Manager | **Always / previous value** |

Voice Recognition Services, the Smart Hub terms, Auto Update, Usage Mode, the Samsung account
and Power On with Mobile were left unchanged, so there is nothing to restore for them.

Full factory restore (last resort, wipes everything): Settings > General > Reset (PIN 0000).
