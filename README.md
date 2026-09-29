<div align="center">

# 🎮 GTA RP — Rockstar Games Status

### A cinematic, long-running Discord Rich Presence for GTA V and RDR2

![Version](https://img.shields.io/badge/version-1.2.0-e63946?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/discord-rich%20presence-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-111827?style=for-the-badge)

**Made by [@hbkvxncent](https://discord.com/users/622835390239473665)**

</div>

> [!IMPORTANT]
> This project controls Discord Rich Presence only. It does **not** install, modify,
> or inject into GTA V, FiveM, or Red Dead Redemption 2.

---

## ✨ What this does

**GTA RP — Rockstar Games Status** gives your Discord profile a living Rockstar
Games presence instead of a static “Playing a game” label. It simulates story
missions, online lobbies, activities, and heists while keeping the status alive
for as long as the script is running.

The current release supports:

| Game | Presence profile | Story content | Online content |
| :--- | :--- | :---: | :---: |
| 🚗 **Grand Theft Auto V Enhanced** | `gta5_gen9` | ✅ | ✅ |
| 🚓 **Grand Theft Auto V Legacy / FiveM** | `gta5` | ✅ | ✅ |
| 🤠 **Red Dead Redemption 2** | `rdr2` | ✅ | ✅ |

## 🌟 Features

- **Auto-reconnect:** Discord can restart or temporarily lose its IPC pipe
  without ending the script.
- **State-preserving reconnects:** the mission, activity, player count, and
  elapsed-time anchor remain intact after Discord comes back.
- **Mission picker:** start Story Mode from the beginning, a mission number, or
  a name search.
- **CLI mission selection:** use `--mission "Chop"` or a partial mission name.
- **Realistic story timers:** short setups, standard missions, long set pieces,
  and finales use different duration ranges.
- **Realistic online timers:** activities rotate naturally instead of staying
  frozen for the entire session.
- **Live terminal status:** see connection state, game, mission/activity, next
  mission countdown, and total elapsed time.
- **Heist simulation:** display a 1–4 player heist status for GTA V.
- **Two-game cycling:** rotate between any two supported games automatically.
- **Cross-platform:** works with Python 3 on Windows, macOS, and Linux.

---

## 📚 Table of contents

- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick start](#-quick-start)
- [Interactive menu](#-interactive-menu)
- [Command-line usage](#-command-line-usage)
- [How the timer works](#-how-the-timer-works)
- [Connection and auto-reconnect](#-connection-and-auto-reconnect)
- [Superman mods by JulioNIB](#-superman-mods-by-julionib)
- [Troubleshooting](#-troubleshooting)
- [Support](#-support)
- [Disclaimer](#-disclaimer)

---

## 📋 Requirements

Before starting, make sure you have:

- **Python 3.8 or newer**
- The **Discord desktop application** installed on the same computer
- The Python package **pypresence**
- An internet connection for Discord IPC and presence artwork

The script does not require GTA V or RDR2 to be running. It simulates the
presence, so you can use it for testing or leave it running alongside a game.

---

## 🚀 Installation

### 1. Install Python

Download Python from [python.org](https://www.python.org/downloads/) if it is
not already installed. During Windows installation, enable **Add Python to
PATH**.

Check your installation:

```bash
python --version
```

If your system uses `python3`, run:

```bash
python3 --version
```

### 2. Install the dependency

Windows:

```powershell
py -m pip install pypresence
```

macOS / Linux:

```bash
python3 -m pip install pypresence
```

If `python` already points to Python 3, this also works:

```bash
python -m pip install pypresence
```

### 3. Save the script

Place the Python file in a folder of your choice and name it:

```text
rpc.py
```

Open a terminal in that folder. For example:

```bash
cd path/to/your/folder
```

### 4. Start Discord

Open the **Discord desktop app** and sign in before launching the script.
Discord can also be started after the script, because v1.2.0 keeps retrying
until the IPC connection becomes available.

---

## ⚡ Quick start

The easiest option is the interactive menu:

```bash
python rpc.py
```

On macOS or Linux:

```bash
python3 rpc.py
```

The menu lets you:

1. Choose GTA V Enhanced, GTA V Legacy / FiveM, or RDR2.
2. Choose Story Mode or Online Mode.
3. Pick a Story Mode starting mission.
4. Optionally simulate a GTA V heist with 1–4 players.
5. Cycle between two games.

Press **Ctrl+C** once to stop the active presence and return to the menu.
Press it again if you want to close the terminal process.

---

## 🕹️ Interactive menu

Run:

```bash
python rpc.py
```

### Story Mode

When Story Mode is selected, choose one of these starting methods:

| Choice | Behavior |
| :---: | :--- |
| `1` | Start from the first mission |
| `2` | Choose a mission by its number from a two-column list |
| `3` | Search the mission list by name, then select a result |

The mission list includes the complete GTA V and RDR2 story mission data
included in the script. After a mission’s simulated duration expires, the
presence advances to the next mission and wraps around at the end.

### Online Mode

Online Mode starts with a short simulated lobby-loading phase. The player count
then fluctuates within the supported lobby size to make the status feel less
static. GTA V can also display a simulated heist with a selected player count.

### Cycling between two games

Choose the cycle option, select two different games, then set the number of
seconds between swaps. The default is **30 seconds**.

---

## 💻 Command-line usage

### Examples

```bash
# Interactive menu
python rpc.py

# GTA V Enhanced Online
python rpc.py --mode enhanced --type online

# GTA V Legacy Story Mode
python rpc.py --mode legacy --type story

# Start GTA V Story Mode at a mission
python rpc.py --mode legacy --type story --mission "Chop"

# Start RDR2 Online
python rpc.py --mode rdr2 --type online

# Simulate a four-player GTA V heist
python rpc.py --mode enhanced --type online --heist 4

# Cycle between GTA V Enhanced and RDR2 every 30 seconds
python rpc.py --mode both --games enhanced,rdr2 --type online --interval 30
```

### Options

| Option | Accepted values | Description |
| :--- | :--- | :--- |
| `--mode` | `enhanced`, `legacy`, `rdr2`, `both`, `menu` | Select one presence or enter cycling/menu mode. Default: `menu`. |
| `--type` | `story`, `online` | Select Story Mode or Online Mode. Default: `online`. |
| `--mission` | Mission name or fragment | Select a Story Mode starting mission. Matching is case-insensitive. |
| `--heist` | `1`, `2`, `3`, `4` | Set the simulated GTA V heist player count. |
| `--games` | Two game keys | Games to cycle when `--mode both` is used. Example: `enhanced,rdr2`. |
| `--interval` | Positive integer | Seconds between game swaps in cycle mode. Default: `30`. |

`--mission` resolves names in this order:

1. Exact match.
2. Unique prefix match.
3. Unique substring match.
4. The first substring match when a search is ambiguous.

If no mission matches, the script warns you and starts from the beginning.

---

## ⏱️ How the timer works

The terminal status line is designed to look like an active, ongoing session:

```text
● LIVE   GTA V Legacy │ Story │ Chop │ next in 08:42 │ 12:34
```

- `● LIVE` means Discord IPC is connected.
- `○ WAIT` means the script is still running but is waiting to reconnect.
- `next in mm:ss` is the remaining simulated duration of the current story
  mission.
- The final timer is the total elapsed session time.

The elapsed-time anchor is created when the session starts. Reconnecting to
Discord does **not** reset it.

### Story Mode duration ranges

| Tier | Approximate duration | Examples |
| :--- | :---: | :--- |
| Ultra-short | 3–7 minutes | Prologue, Chop, setups, masks, rampages |
| Short | 6–12 minutes | Father/Son, Friend Request, A Quiet Time |
| Long | 15–25 minutes | Blitz Play, Mr. Philips, major set pieces |
| Epic | 25–45 minutes | Jewel Store Job, Paleto Score, The Big Score, finales |
| Standard | 10–20 minutes | Missions without a more specific category |

Standard missions receive additional late-game scaling so the final portion of
a story does not feel artificially rushed.

### Online activity duration ranges

| Activity type | Approximate duration |
| :--- | :---: |
| Heists, finales, casino, and similar activities | 15–60 minutes |
| Bounties, trading, selling, missions, survivals | 5–15 minutes |
| Racing, freemode, hunting, fishing, camping | 3–10 minutes |

These are simulated display timers, not measurements of a real game session.

---

## 🔄 Connection and auto-reconnect

Version 1.2.0 changes the script from a one-shot presence setter into a
long-running session:

- A failed initial connection is non-fatal.
- If Discord closes, crashes, sleeps, or loses its IPC pipe, the status changes
  from `● LIVE` to `○ WAIT`.
- Reconnect attempts use exponential backoff:
  **5 seconds → 10 seconds → 20 seconds → 40 seconds → up to 60 seconds**.
- When Discord returns, the presence is pushed again automatically.
- The mission index, online activity, player count, mission start time, and
  session timer are preserved.
- The keepalive loop refreshes the presence every **15 seconds**.

You can safely start `rpc.py` before Discord if you want; the script will keep
waiting instead of exiting immediately.

---

## 🦸 Superman mods by [JulioNIB](https://www.patreon.com/cw/JulioNIB)

The RPC script and GTA V mods are separate projects. The links below are
included as a convenience for anyone setting up JulioNIB-style superhero mods.
**Follow every step in the installation guide for your game version** so you do
not damage your GTA V installation.

> [!WARNING]
> Install and use mods in **Story Mode only**. Do not enter GTA Online with
> mod files installed. Make a backup of your game files first, install one mod
> at a time, and keep a clean, unmodded launch path available.

### Mod showcase

<div align="center">
  <a href="https://www.youtube.com/watch?v=KGqys3Aoh04">
    <img src="https://i.ytimg.com/vi/KGqys3Aoh04/hqdefault.jpg" alt="Homelander GTA 5 mod video" width="560">
  </a>
  <br>
  <strong>Homelander GTA 5 mod</strong>
  <br>
  <a href="https://www.youtube.com/watch?v=KGqys3Aoh04">▶ Watch the showcase on YouTube</a>
</div>

### Homelander GTA 5 mod — Part 2

<div align="center">
  <a href="https://www.youtube.com/watch?v=S_lKpTTe4PM">
    <img src="https://i.ytimg.com/vi/S_lKpTTe4PM/hqdefault.jpg" alt="Homelander GTA 5 mod part 2 video" width="560">
  </a>
  <br>
  <strong>Homelander gta5 mod pt.2</strong>
  <br>
  <a href="https://www.youtube.com/watch?v=S_lKpTTe4PM">▶ Watch Part 2 on YouTube</a>
</div>

### Complete setup guide

<div align="center">
  <a href="https://www.youtube.com/watch?v=K6PjDEzlfTw">
    <img src="https://i.ytimg.com/vi/K6PjDEzlfTw/hqdefault.jpg" alt="GTA 5 Legacy complete JulioNIB mods setup guide" width="560">
  </a>
  <br>
  <strong>GTA 5 Legacy — Complete Setup guide for my mods (JulioNIB Mods - 2025)</strong>
  <br>
  <a href="https://www.youtube.com/watch?v=K6PjDEzlfTw">▶ Watch the complete setup guide on YouTube</a>
</div>

### Safer mod-install checklist

1. Confirm whether the mod is for **GTA V Legacy** or **GTA V Enhanced**.
2. Back up the original files before changing anything.
3. Follow the setup guide from start to finish instead of copying only part of
   the installation.
4. Install required loaders, menus, scripts, and suits exactly as the guide
   describes.
5. Test the mod in Story Mode before adding another mod.
6. If Story Mode mods require it, disable **BattlEye** as a personal
   precaution according to your launcher/setup instructions.
7. Never use the modded installation to join GTA Online.
8. If the game stops launching, remove the newest change or restore your clean
   backup before troubleshooting further.

The BattlEye note is a safety precaution for modded offline play, not a
guarantee about Rockstar’s detection systems. Always follow the current
instructions from the mod author and your game launcher.

---

## 🧰 Troubleshooting

### `Missing pypresence`

Install the dependency with the same Python interpreter you use to run the
script:

```bash
python -m pip install pypresence
```

On Windows, try:

```powershell
py -m pip install pypresence
```

### The status says `○ WAIT`

This is expected when Discord is closed or its IPC service is unavailable.

1. Open the Discord **desktop** app.
2. Confirm you are signed in.
3. Wait for the next reconnect attempt.
4. If needed, restart Discord; the script should recover without losing its
   mission or timer state.

### The status does not appear on Discord

- Confirm the script is still running in the terminal.
- Confirm Discord is the desktop app, not only a browser tab.
- Check Discord’s activity/privacy settings.
- Stop other Rich Presence tools that may be competing for the same status.
- Restart Discord and let the script reconnect.

### The game artwork is missing

The artwork is provided through the configured Discord applications. Give
Discord a moment to refresh, then reconnect or restart Discord if the status
text appears without artwork.

### I want to stop the script

Press **Ctrl+C**. The script clears the presence and closes its IPC connection
cleanly.

---

## 💬 Support

If you find a bug or need help, include:

- Your operating system
- Your Python version
- The command you ran
- The complete terminal error
- Whether Discord was open when the script started

Contact:

- **Discord:** [@hbkvxncent](https://discord.com/users/622835390239473665)
- **Email:** [support@globalstats.xyz](mailto:support@globalstats.xyz)

---

## ⚠️ Disclaimer

This is an unofficial community project and is not affiliated with Rockstar
Games, Take-Two Interactive, FiveM, Discord, or JulioNIB.

The Client IDs currently used by the script are associated with Rockstar Games
and FiveM, not the author. Connecting with another party’s Discord Application
ID may be considered impersonation and may conflict with Discord’s Terms of
Service. Use the script at your own risk, or replace the IDs with a Discord
application that you control.

GTA V and Red Dead Redemption 2 are trademarks of their respective owners.
Mod installation instructions and third-party videos belong to their
respective authors. Always keep a clean game backup and never use modded files
in GTA Online.

---

<div align="center">

**GTA RP — Rockstar Games Status** · `v1.2.0`

</div>
