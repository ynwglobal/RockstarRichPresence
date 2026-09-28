"""
gta5_rpc.py
Set Discord Rich Presence to look like GTA V Enhanced, GTA V Legacy / FiveM,
or Red Dead Redemption 2 — now with realistic story missions, offline activities,
dynamic online modes, heist simulation, and correct images.

USAGE
-----
Interactive menu:
    python rpc.py

Direct:
    python rpc.py --mode enhanced --type online
    python rpc.py --mode legacy --type story
    python rpc.py --mode rdr2 --type online
    python rpc.py --mode both --games enhanced,rdr2 --type online --interval 30

Requires:  pip install pypresence
Discord desktop app must be running.

NOTE: The Client IDs below belong to Rockstar / FiveM, not to you.
Connecting with someone else's Application ID is impersonation and
is against Discord's ToS. Use at your own risk.
"""

import argparse
import os
import sys
import time
import random

try:
    from pypresence import Presence, ActivityType
except ImportError:
    print("[!] Missing pypresence. Install with:  pip install pypresence")
    sys.exit(1)


# ---------------------------------------------------------------
# Enable ANSI escape sequences on Windows consoles
# ---------------------------------------------------------------
if os.name == "nt":
    os.system("")


# ---------------------------------------------------------------
# ANSI palette
# ---------------------------------------------------------------
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

GREEN   = "\033[38;5;46m"     # GTA V Enhanced
ORANGE  = "\033[38;5;208m"    # GTA V Legacy / FiveM
RED     = "\033[38;5;203m"    # Red Dead Redemption 2
YELLOW  = "\033[38;5;221m"    # menu numbers
GRAY    = "\033[38;5;243m"    # chrome / borders
WHITE   = "\033[97m"
HOTPINK = "\033[38;5;205m"    # author tag


def c(text, *styles):
    """Wrap text in ANSI styles and reset afterwards."""
    return "".join(styles) + str(text) + RESET


# ---------------------------------------------------------------
# Author / version info
# ---------------------------------------------------------------
VERSION = "v.1.0.0"
AUTHOR  = "@hbkvxncent"
SUPPORT_EMAIL = "support@globalstats.xyz"


def banner():
    bar = c("=" * 64, GRAY)
    print()
    print(bar)
    print(c("  DISCORD RICH PRESENCE", BOLD, WHITE) +
          "    " + c(VERSION, BOLD, HOTPINK))
    print(c("  made by ", GRAY) + c(AUTHOR, BOLD, HOTPINK))
    print(bar)


def support_note():
    print()
    print(c("  Need help or found a bug?", BOLD, YELLOW))
    print(c("  Message ", GRAY) + c(AUTHOR, BOLD, HOTPINK) +
          c(" on Discord or email ", GRAY) +
          c(SUPPORT_EMAIL, BOLD, WHITE))
    print(c("  I will look into it and get back with an answer or a fix.", GRAY))
    print()


# ---------------------------------------------------------------
# Mission & Activity Data
# ---------------------------------------------------------------
GTA_V_STORY_MISSIONS = [
    "Prologue", "Franklin and Lamar", "Repossession", "Complications",
    "Father/Son", "Chop", "Marriage Counseling", "Daddy's Little Girl",
    "Friend Request", "The Long Stretch", "The Good Husband",
    "Casing the Jewel Store", "Carbine Rifles", "Bugstars Equipment",
    "BZ Gas Grenades", "The Jewel Store Job (Loud)", "The Jewel Store Job (Smart)",
    "Mr. Philips", "Trevor Philips Industries", "Nervous Ron",
    "Crystal Maze", "Friends Reunited", "Fame Or Shame",
    "Dead Man Walking", "Three's Company", "By the Book",
    "Hood Safari", "Did Somebody Say Yoga?", "Scouting the Port",
    "Minisub", "Cargobob", "The Merryweather Heist (Offshore)",
    "The Merryweather Heist (Freighter)", "The Hotel Assassination",
    "Boiler Suits", "Masks", "Trash Truck", "Tow Truck", "Blitz Play",
    "I Fought the Law...", "Eye in the Sky", "Mr. Richards",
    "Caida Libre", "Deep Inside", "Minor Turbulence",
    "Paleto Score Setup", "Predator", "Military Hardware",
    "The Paleto Score", "Derailed", "Monkey Business", "Hang Ten",
    "Surveying the Score", "Bury the Hatchet", "Pack Man",
    "Fresh Meat", "The Ballad of Rocco", "Cleaning out the Bureau",
    "Architect's Plans", "Fire Truck", "The Bureau Raid (Fire Crew)",
    "The Bureau Raid (Roof Entry)", "The Wrap Up",
    "Reuniting the Family", "Doting Dad", "Legal Trouble",
    "Lamar Down", "Meltdown", "Parenting 101", "Planning The Big Score",
    "Stingers", "Sidetracked", "Gauntlet (1-3)", "Driller",
    "The Big Score (Subtle)", "The Big Score (Obvious)",
    "Something Sensible (Ending A)", "The Time's Come (Ending B)",
    "The Third Way (Ending C)"
]

GTA_V_ONLINE_ACTIVITIES = [
    "Online Mission", "Online Racing", "Freemode", "Heist Setup",
    "Business Battle", "Selling Goods", "Deathmatch", "Survival"
]

RDR2_STORY_MISSIONS = [
    # Chapter 1: Colter
    "Outlaws from the West", "Enter, Pursued by a Memory",
    "The Aftermath of Genesis", "Old Friends",
    "Who the Hell is Leviticus Cornwall?", "Eastward Bound",
    # Chapter 2: Horseshoe Overlook
    "Polite Society, Valentine Style", "Americans at Rest",
    "Who is Not without Sin", "Exit Pursued by a Bruised Ego",
    "The First Shall be Last", "Paying a Social Call",
    "A Quiet Time", "Blessed are the Meek?", "Good, Honest, Snake Oil",
    "We Loved Once and True (I, II, III)", "Money Lending and Other Sins I & II",
    "Money Lending and Other Sins III", "The Spines of America",
    "Pouring Forth Oil (I & II)", "Pouring Forth Oil III & IV",
    "A Fisher of Men", "An American Pastoral Scene",
    "The Sheep and the Goats", "A Strange Kindness",
    # Chapter 3: Clemens Point
    "The New South", "Further Questions of Female Suffrage",
    "Money Lending and Other Sins IV", "American Distillation",
    "The Course of True Love I & II", "The Course of True Love III",
    "Advertising, the New American Art (I & II)", "Horse Flesh for Dinner",
    "The Fine Joys of Tobacco", "Magicians for Sport",
    "Friends in Very Low Places", "An Honest Mistake",
    "Preaching Forgiveness As He Went", "Sodom? Back to Gomorrah",
    "Blessed are the Peacemakers", "A Short Walk in a Pretty Town",
    "Blood Feuds, Ancient and Modern", "The Battle of Shady Belle",
    # Chapter 4: Shady Belle
    "The Joys of Civilization", "Angelo Bronte, a Man of Honor",
    "Money Lending and Other Sins V", "Help a Brother Out",
    "Brothers and Sisters, One and All", "Fatherhood and Other Dreams (I & II)",
    "No, No and Thrice, No", "The Gilded Cage",
    "A Fine Night of Debauchery", "American Fathers (I & II)",
    "High and Low Finance", "Horsemen, Apocalypses",
    "Urban Pleasures", "Country Pursuits",
    "Revenge is a Dish Best Eaten", "Banking, the Old American Art",
    # Chapter 5: Guarma
    "Welcome to the New World", "Savagery Unleashed",
    "A Kind and Benevolent Despot", "Hell Hath No Fury",
    "Paradise Mercifully Departed", "Dear Uncle Tacitus",
    "Fleeting Joy", "A Fork in the Road", "That's Murfree Country",
    # Chapter 6: Beaver Hollow
    "Icarus and Friends", "Visiting Hours", "Just a Social Call",
    "Do Not Seek Absolution I", "Do Not Seek Absolution II",
    "Of Men And Angels", "The Course of True Love IV & V",
    "Money Lending and Other Sins VI & VII", "The Delights of Van Horn",
    "The Bridge to Nowhere", "A Rage Unleashed",
    "Archaeology for Beginners", "Honor, Amongst Thieves",
    "The Fine Art of Conversation", "Goodbye, Dear Friend",
    "Mrs. Sadie Adler, Widow (I & II)", "Favored Sons",
    "The King's Son", "My Last Boy", "Our Best Selves",
    "Red Dead Redemption",
    # Epilogue Part 1: Pronghorn Ranch
    "The Wheel", "Simple Pleasures", "Farming, for Beginners",
    "Fatherhood, for Beginners", "Old Habits",
    "Jim Milton Rides, Again?", "Fatherhood, for Idiots",
    "Motherhood", "Gainful Employment",
    "The Landowning Classes / Home of the Gentry?",
    # Epilogue Part 2: Beecher's Hope
    "Bare Knuckles Friendships", "Home Improvement for Beginners",
    "An Honest Day's Labors", "The Tool Box", "A New Jerusalem",
    "A Quick Favor for an Old Friend", "Uncle's Bad Day",
    "Trying Again", "A Really Big Bastard",
    "A New Future Imagined", "American Venom"
]

RDR2_ONLINE_ACTIVITIES = [
    "Moseying in Emerald Ranch", "Hunting in Valentine",
    "Camping in the Heartlands", "Fishing in Flat Iron Lake",
    "Bounty Hunting in New Hanover", "Trading in Saint Denis"
]

# ---------------------------------------------------------------
# Game registry
# ---------------------------------------------------------------
GAMES = {
    "enhanced": {
        "label":     "Grand Theft Auto V Enhanced",
        "short":     "GTA V Enhanced",
        "client_id": "1329870933695135785",   # gta5_gen9
        "title_id":  "gta5_gen9",
        "large_image_story": "gta5_enhanced",       # Story Mode logo
        # Using the full CDN URL ensures the image loads correctly for Enhanced
        "large_image_online": "https://cdn.discordapp.com/app-assets/1329870933695135785/1342577565122170972.png",
        "details_story": "Playing story",
        "details_online": "Grand Theft Auto V Enhanced",
        "missions": GTA_V_STORY_MISSIONS,
        "activities": GTA_V_ONLINE_ACTIVITIES,
        "max_players": 32,
        "color":     GREEN,
    },
    "legacy": {
        "label":     "Grand Theft Auto V Legacy / FiveM",
        "short":     "GTA V Legacy",
        "client_id": "356876176465199104",    # FiveM / gta5
        "title_id":  "gta5",
        "large_image_story": "gta5",                # Story Mode logo
        # Using the same GTA Online CDN URL as Enhanced
        "large_image_online": "https://cdn.discordapp.com/app-assets/1329870933695135785/1342577565122170972.png",
        "details_story": "Playing story",
        "details_online": "Grand Theft Auto V Legacy",
        "missions": GTA_V_STORY_MISSIONS,
        "activities": GTA_V_ONLINE_ACTIVITIES,
        "max_players": 32,
        "color":     ORANGE,
    },
    "rdr2": {
        "label":     "Red Dead Redemption 2",
        "short":     "RDR2",
        "client_id": "643897785271189524",    # rdr2
        "title_id":  "rdr2",
        "large_image_story": "rdr2",                # Story Mode logo
        "large_image_online": "rdr2_online",        # Red Dead Online logo
        "details_story": "Playing Red Dead Redemption 2",
        "details_online": "Playing Red Dead Online",
        "missions": RDR2_STORY_MISSIONS,
        "activities": RDR2_ONLINE_ACTIVITIES,
        "max_players": 32,
        "color":     RED,
    },
}

ORDER = ["enhanced", "legacy", "rdr2"]   # menu order


# ---------------------------------------------------------------
# RPC session wrapper
# ---------------------------------------------------------------
class RPCSession:
    def __init__(self, game: str, mode: str = "online", start_mission: str = None, heist_players: int = None):
        if game not in GAMES:
            raise ValueError(f"Unknown game: {game}")
        self.game = game
        self.mode = mode  # "story" or "online"
        self.info = GAMES[game]
        self.presence = None
        self.start_ts = int(time.time())
        self.max_players = self.info["max_players"]
        self.heist_players = heist_players # <--- Store heist players
        
        # Player count simulation variables
        self.session_players = 0
        self.is_loading = (self.mode == "online")
        self.loading_target = random.randint(12, 24)
        self.last_update = time.time()

        # Story mission tracking
        self.missions = self.info["missions"]
        if start_mission and start_mission in self.missions:
            self.mission_index = self.missions.index(start_mission)
        else:
            self.mission_index = 0
        
        self.mission_start_time = time.time()
        # Realistic mission duration: 15 to 30 minutes (900 to 1800 seconds)
        self.mission_duration = random.randint(900, 1800)
        self.current_activity = random.choice(self.info["activities"]) if self.mode == "online" else None

    def _fluctuate_session(self):
        """Simulates joining a session and then realistic player count changes."""
        if self.mode == "story":
            return

        current_time = time.time()
        if current_time - self.last_update < 5:
            return
        self.last_update = current_time

        if self.is_loading:
            self.session_players += random.randint(1, 4)
            if self.session_players >= self.loading_target:
                self.is_loading = False
                self.session_players = random.randint(15, self.max_players - 2)
        else:
            if random.random() < 0.3:
                return
            change = random.randint(-3, 3)
            self.session_players = max(1, min(self.max_players, self.session_players + change))

    def _update_story_mission(self):
        """Updates the story mission realistically over time."""
        if self.mode == "story":
            current_time = time.time()
            if current_time - self.mission_start_time > self.mission_duration:
                # Advance to next mission or loop back
                self.mission_index = (self.mission_index + 1) % len(self.missions)
                self.mission_start_time = current_time
                # Reset duration for the next mission
                self.mission_duration = random.randint(900, 1800)

    def connect(self):
        info = self.info
        mode_str = "Online" if self.mode == "online" else "Story"
        print(c("  > ", info["color"]) +
              c(info["label"], BOLD, info["color"]) + 
              c(f" ({mode_str})", DIM, GRAY))
        print(c(f"    client_id={info['client_id']}  "
                f"title_id={info['title_id']}", DIM, GRAY))

        try:
            self.presence = Presence(info["client_id"])
            self.presence.connect()
        except Exception as e:
            print(c(f"\n[!] Could not connect to Discord IPC: {e}", RED))
            print(c("    -> Is the Discord desktop app open and running?\n", GRAY))
            raise

        self.start_ts = int(time.time())
        self._push()

    def _push(self):
        self._fluctuate_session()
        self._update_story_mission()
        
        if self.mode == "story":
            details = self.info["details_story"]
            # For GTA V, state is the mission. For RDR2, state is the mission.
            if self.game in ["enhanced", "legacy"]:
                state = self.missions[self.mission_index]
            else:
                state = self.missions[self.mission_index] # RDR2 missions
            large_image = self.info["large_image_story"]
        else:
            details = self.info["details_online"]
            
            # Check if we are in Heist Mode
            if self.heist_players is not None:
                state = f"Heist ({self.heist_players} of 4)"
            else:
                # Formatting the state to look like the official RPC
                if self.game in ["enhanced", "legacy"]:
                    # Randomly show either player count or an Online Activity
                    if random.random() < 0.5:
                        state = f"GTA Online ({self.session_players} of {self.max_players})"
                    else:
                        state = self.current_activity
                else:
                    # RDR2 Online
                    state = f"Red Dead Online ({self.session_players} of {self.max_players})"
                    if random.random() < 0.5:
                        state = self.current_activity
                        
            large_image = self.info["large_image_online"]

        # Set up buttons similar to the official Rockstar RPC
        buttons = [
            {"label": "Ask to Join", "url": "https://discord.com"},
            {"label": "Get on Steam", "url": "https://store.steampowered.com"}
        ]

        self.presence.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            start=self.start_ts,
            large_image=large_image,
            large_text=self.info["label"],
            buttons=buttons
        )

    def keepalive(self):
        """Ping Discord so the presence doesn't drop."""
        self._push()

    def close(self):
        if self.presence is None:
            return
        try:
            self.presence.clear()
        except Exception:
            pass
        try:
            self.presence.close()
        except Exception:
            pass
        self.presence = None
        print(c("  - presence cleared.", DIM, GRAY))


# ---------------------------------------------------------------
# Runners
# ---------------------------------------------------------------
def run_single(game: str, mode: str = "online", start_mission: str = None, heist_players: int = None):
    info = GAMES[game]
    session = RPCSession(game, mode, start_mission, heist_players)
    try:
        session.connect()
    except Exception as e:
        print(c(f"\n[!] Connection failed: {e}", RED))
        session.close()
        return

    mode_str = "Online" if mode == "online" else "Story"
    print(c(f"[OK] Presence set to '{info['short']}' ({mode_str}). "
            f"Ctrl+C to stop.", BOLD, info["color"]))
    print()
    try:
        while True:
            time.sleep(15) # Update every 15 seconds
            session.keepalive()
    except KeyboardInterrupt:
        print()
    finally:
        session.close()


def run_cycle(games, interval: int, modes: dict, missions: dict, heist_map: dict):
    joined = c(" <-> ", GRAY).join(
        c(GAMES[g]["short"], BOLD, GAMES[g]["color"]) for g in games
    )
    print(c(f"[*] Cycling between {joined} ", GRAY) +
          c(f"every {interval}s.", GRAY))
    print(c("    Ctrl+C to stop and go back to the menu.", GRAY))
    print()

    current = None
    try:
        while True:
            for game in games:
                if current is not None:
                    current.close()
                current = RPCSession(game, modes[game], missions.get(game), heist_map.get(game))
                current.connect()
                time.sleep(interval)
    except KeyboardInterrupt:
        print()
    finally:
        if current is not None:
            current.close()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
def show_menu():
    bar = c("-" * 64, GRAY)
    print()
    print(bar)
    print(c("  DISCORD RICH PRESENCE", BOLD, WHITE) + c("  |  ", GRAY) +
          c("GTA V", BOLD, GREEN) + c(" / ", GRAY) + c("RDR2", BOLD, RED))
    print(bar)

    for i, key in enumerate(ORDER, 1):
        info = GAMES[key]
        label = info["label"].ljust(38)
        print(f"   {c(str(i), BOLD, YELLOW)})  "
              f"{c(label, info['color'])} "
              f"{c('(' + info['title_id'] + ')', DIM, GRAY)}")

    print(f"   {c('4', BOLD, YELLOW)})  "
          f"{c('Cycle between TWO games...', WHITE)}")
    print(f"   {c('q', BOLD, YELLOW)})  {c('Quit', WHITE)}")
    print(bar)
    return input(c("  Choice: ", BOLD, WHITE)).strip().lower()


def ask_mode(game_key):
    info = GAMES[game_key]
    print(f"\n  Selected: {c(info['short'], BOLD, info['color'])}")
    print(f"   {c('1', BOLD, YELLOW)}) Story Mode")
    print(f"   {c('2', BOLD, YELLOW)}) Online Mode {c('(with realistic session loading)', DIM, GRAY)}")
    choice = input(c("  Choice [2]: ", BOLD, WHITE)).strip()
    
    if choice == "1":
        # Ask for specific mission
        print(f"\n  Story Mode selected. Do you want to start from the beginning or choose a specific mission?")
        print(f"   {c('1', BOLD, YELLOW)}) Start from beginning (Prologue / Chapter 1)")
        print(f"   {c('2', BOLD, YELLOW)}) Choose a specific mission")
        sub_choice = input(c("  Choice [1]: ", BOLD, WHITE)).strip()
        
        if sub_choice == "2":
            print(f"\n  Available missions for {info['short']}:")
            for i, mission in enumerate(info["missions"], 1):
                print(f"   {c(str(i), BOLD, YELLOW)}) {mission}")
            try:
                m_choice = int(input(c("  Enter mission number: ", BOLD, WHITE)).strip())
                if 1 <= m_choice <= len(info["missions"]):
                    return "story", info["missions"][m_choice - 1], None
            except ValueError:
                pass
            print(c("[!] Invalid choice. Starting from beginning.", RED))
        return "story", info["missions"][0], None
        
    else:
        # Online Mode - Ask about Heist for GTA V only
        heist_players = None
        if game_key in ["enhanced", "legacy"]:
            print(f"\n  Do you want to simulate a Heist?")
            print(f"   {c('1', BOLD, YELLOW)}) Yes (Heist with players)")
            print(f"   {c('2', BOLD, YELLOW)}) No (Regular Online)")
            heist_choice = input(c("  Choice [2]: ", BOLD, WHITE)).strip()
            
            if heist_choice == "1":
                raw = input(c("  How many players? (1-4) or Enter for auto (2/3/4): ", GRAY)).strip()
                if raw.isdigit() and 1 <= int(raw) <= 4:
                    heist_players = int(raw)
                else:
                    heist_players = random.choice([2, 3, 4])
                    print(c(f"  Auto-selected: {heist_players} players", DIM, GRAY))
                    
        return "online", None, heist_players


def pick_two():
    print()
    for i, key in enumerate(ORDER, 1):
        info = GAMES[key]
        print(f"   {c(str(i), BOLD, info['color'])}) "
              f"{c(info['label'], info['color'])}")
    print()

    prompt = (c("  Pick TWO games", BOLD, WHITE) + c(" (e.g. ", GRAY) +
              c("1 3", YELLOW) + c("): ", GRAY))
    raw = input(prompt).strip()
    if not raw:
        return None

    tokens = [t for t in raw.replace(",", " ").split() if t]
    if len(tokens) == 1 and len(tokens[0]) == 2 and tokens[0].isdigit():
        tokens = list(tokens[0])

    picked = []
    for t in tokens:
        if not t.isdigit() or not (1 <= int(t) <= len(ORDER)):
            print(c("[!] Invalid selection.", RED))
            return None
        key = ORDER[int(t) - 1]
        if key in picked:
            print(c("[!] Pick two DIFFERENT games.", RED))
            return None
        picked.append(key)

    if len(picked) != 2:
        print(c("[!] You must pick exactly two games.", RED))
        return None

    return picked


def ask_interval(default: int = 30):
    raw = input(c(f"  Swap every how many seconds? [{default}]: ", GRAY)).strip()
    if raw.isdigit() and int(raw) > 0:
        return int(raw)
    return default


def interactive():
    while True:
        choice = show_menu()

        if choice in ("q", "quit", "exit"):
            print(c("[*] Bye.", GRAY))
            return

        try:
            if choice in ("1", "2", "3"):
                game = ORDER[int(choice) - 1]
                mode, mission, heist_players = ask_mode(game)
                run_single(game, mode, mission, heist_players)
            elif choice == "4":
                picked = pick_two()
                if not picked:
                    continue
                modes = {}
                missions = {}
                heist_map = {}
                for g in picked:
                    m, ms, hp = ask_mode(g)
                    modes[g] = m
                    missions[g] = ms
                    heist_map[g] = hp
                interval = ask_interval()
                run_cycle(picked, interval, modes, missions, heist_map)
            else:
                print(c("[!] Invalid choice.", RED))
        except KeyboardInterrupt:
            print()
        except Exception as e:
            print(c(f"[!] {e}", RED))


# ---------------------------------------------------------------
# CLI
# ---------------------------------------------------------------
def parse_games(s: str):
    parts = [p.strip().lower()
             for p in s.replace(" ", ",").split(",") if p.strip()]
    for p in parts:
        if p not in GAMES:
            raise argparse.ArgumentTypeError(
                f"unknown game '{p}'. Options: {', '.join(ORDER)}"
            )
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            "need exactly two games, e.g. --games enhanced,rdr2"
        )
    if parts[0] == parts[1]:
        raise argparse.ArgumentTypeError("pick two different games")
    return parts


def main():
    ap = argparse.ArgumentParser(
        description="GTA V / RDR2 Discord Rich Presence"
    )
    ap.add_argument(
        "--mode",
        choices=["enhanced", "legacy", "rdr2", "both", "menu"],
        default="menu",
        help="Which presence to set (default: interactive menu)",
    )
    ap.add_argument(
        "--type",
        choices=["story", "online"],
        default="online",
        help="Play mode: story or online (default: online)",
    )
    ap.add_argument(
        "--mission",
        type=str,
        default=None,
        help="Specific mission to start from in Story Mode",
    )
    ap.add_argument(
        "--heist",
        type=int,
        choices=[1, 2, 3, 4],
        default=None,
        help="Number of players for a simulated Heist (1-4)",
    )
    ap.add_argument(
        "--games",
        type=parse_games,
        default=None,
        help="Two games to cycle with --mode both, e.g. enhanced,rdr2",
    )
    ap.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between swaps when cycling (default: 30)",
    )
    args = ap.parse_args()

    banner()
    support_note()

    try:
        if args.mode == "menu":
            interactive()
        elif args.mode == "both":
            games = args.games or ["enhanced", "legacy"]
            modes = {g: args.type for g in games}
            missions = {g: args.mission for g in games}
            heist_map = {g: args.heist for g in games}
            run_cycle(games, args.interval, modes, missions, heist_map)
        else:
            run_single(args.mode, args.type, args.mission, args.heist)
    except KeyboardInterrupt:
        print(c("\n[*] Interrupted.", GRAY))
    except Exception as e:
        print(c(f"\n[!] Fatal: {e}", RED))
        sys.exit(1)


if __name__ == "__main__":
    main()