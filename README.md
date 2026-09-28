<div align="center">

# 🎮 GTA RP — Rockstar Games Status

### Show off your Rockstar sessions with a polished Discord Rich Presence

![Version](https://img.shields.io/badge/version-1.0.0-1E90FF?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/discord-rich%20presence-5865F2?style=for-the-badge&logo=discord&logoColor=white)

**Made by [@hbkvxncent](https://discord.com/users/622835390239473665)**

</div>

---

## ✨ Overview

**GTA RP** brings a cinematic Rockstar Games status to your Discord profile. It supports three titles:

| Game | Platform |
| --- | --- |
| 🚗 **Grand Theft Auto V Enhanced** | Enhanced Edition |
| 🚓 **Grand Theft Auto V Legacy** | Legacy Edition and FiveM |
| 🤠 **Red Dead Redemption 2** | Story and Online |

### Features

- 🎬 **Story missions** that advance on a realistic timer, so your status looks natural over long sessions
- 🌐 **Online sessions** with live-feeling lobby loading and a player count that rises and falls like the real thing
- 💰 **Heist simulation** with a status line for 1 to 4 players
- 🖼️ **Accurate artwork** for every title
- 🔄 **Game cycling** to rotate between two titles automatically

---

## 📋 Requirements

- Python **3.8** or newer
- The **Discord desktop app**, running on the same machine
- The **pypresence** library

---

## 🚀 Installation

1. Install Python from [python.org](https://www.python.org/downloads/) if you don't already have it.
2. Open a terminal or command prompt.
3. Install the required package:

   ```bash
   pip install pypresence
   ```

4. Save the script to your computer as `rpc.py`.

---

## 🕹️ Usage

### Interactive menu

```bash
python rpc.py
```

A menu will guide you through picking a game, choosing **Story** or **Online** mode, selecting a starting mission, or simulating a heist.

### Direct commands

```bash
python rpc.py --mode enhanced --type online
python rpc.py --mode legacy --type story
python rpc.py --mode rdr2 --type online
python rpc.py --mode both --games enhanced,rdr2 --type online --interval 30
```

### Command line options

| Option | Description |
| --- | --- |
| `--mode` | Choose `enhanced`, `legacy`, `rdr2`, `both`, or `menu` |
| `--type` | Choose `story` or `online` |
| `--mission` | Start Story Mode from a specific mission name |
| `--heist` | Set the player count for a simulated heist (1 to 4) |
| `--games` | Pick two games to cycle through when using `--mode both` |
| `--interval` | Seconds between swaps when cycling games |

---

## ⚙️ How It Works

- **Story Mode:** missions progress on a realistic timer, so your presence never looks static.
- **Online Mode:** simulates joining a session with a live player count, then fluctuates it the way a real lobby would.
- **Heist Mode:** displays a heist status line showing the number of players you chose.

---

## 💬 Support

Running into errors or issues? Reach out and I'll get back to you with an answer or a fix.

- **Discord:** [@hbkvxncent](https://discord.com/users/622835390239473665)
- **Email:** support@globalstats.xyz

---

## **⚠️ Disclaimer**

**The Client IDs used in this script belong to Rockstar Games and FiveM, not to the author. Connecting with someone else's Application ID is considered impersonation and goes against the Discord Terms of Service. Use at your own risk.**

---

<div align="center">

**GTA RP — Rockstar Games Status** · v1.0.0

</div>
