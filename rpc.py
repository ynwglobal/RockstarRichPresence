"""
gta5_rpc.py
Set Discord Rich Presence to look like GTA V Enhanced, GTA V Legacy / FiveM,
or Red Dead Redemption 2 — with realistic story missions, offline activities,
dynamic online modes, heist simulation, and correct images.

Now with:
  * Auto-reconnect — if Discord closes/restarts, the presence is paused
    and resumed with the SAME mission / activity / session state.
  * Realistic mission durations — missions scale by type (short setup,
    standard mission, epic heist/finale) and chapter progression.
  * Start Story Mode from ANY mission (number, name search, or CLI flag).
  * Live status line showing connection state, current mission, elapsed time.

USAGE
-----
Interactive menu:
    python rpc.py

Direct:
    python rpc.py --mode enhanced --type online
    python rpc.py --mode legacy --type story --mission "Chop"
    python rpc.py --mode rdr2 --type online
    python rpc.py --mode both --games enhanced,rdr2 --type online --interval 30

Requires:  pip install pypresence
Discord desktop app must be running (it can also be started later — we'll wait).

NOTE: The Client IDs below belong to Rockstar / FiveM, not to you.
Connecting with someone else's Application ID is impersonation and
is against Discord's ToS. Use at your own risk.
"""

import argparse
import os
import sys
import time
import random
import shutil

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

GREEN   = "\033[38;5;46m"
ORANGE  = "\033[38;5;208m"
RED     = "\033[38;5;203m"
YELLOW  = "\033[38;5;221m"
GRAY    = "\033[38;5;243m"
WHITE   = "\033[97m"
HOTPINK = "\033[38;5;205m"
CYAN    = "\033[38;5;81m"
BLUE    = "\033[38;5;75m"


def c(text, *styles):
    return "".join(styles) + str(text) + RESET


def term_width(default: int = 64) -> int:
    try:
        return min(shutil.get_terminal_size((default, 24)).columns, 100)
    except Exception:
        return default


def hrule(char: str = "─", color: str = GRAY, width: int = None) -> str:
    if width is None:
        width = term_width()
    return c(char * width, color)


# ---------------------------------------------------------------
# Author / version info
# ---------------------------------------------------------------
VERSION = "v.1.2.0"
AUTHOR  = "@hbkvxncent"
SUPPORT_EMAIL = "support@globalstats.xyz"


def banner():
    w = term_width()
    print()
    print(c("╭" + "─" * (w - 2) + "╮", GRAY))
    title = "DISCORD RICH PRESENCE"
    tag   = VERSION
    padding = max(1, w - 4 - len(title) - len(tag))
    print(c("│ ", GRAY) + c(title, BOLD, WHITE) +
          " " * padding + c(tag, BOLD, HOTPINK) + c(" │", GRAY))
    made = f"crafted by {AUTHOR}"
    pad2 = max(1, w - 4 - len(made))
    print(c("│ ", GRAY) + c("crafted by ", GRAY) + c(AUTHOR, BOLD, HOTPINK) +
          " " * pad2 + c("│", GRAY))
    print(c("╰" + "─" * (w - 2) + "╯", GRAY))


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
    "Outlaws from the West", "Enter, Pursued by a Memory",
    "The Aftermath of Genesis", "Old Friends",
    "Who the Hell is Leviticus Cornwall?", "Eastward Bound",
    "Polite Society, Valentine Style", "Americans at Rest",
    "Who is Not without Sin", "Exit Pursued by a Bruised Ego",
    "The First Shall be Last", "Paying a Social Call",
    "A Quiet Time", "Blessed are the Meek?", "Good, Honest, Snake Oil",
    "We Loved Once and True (I, II, III)", "Money Lending and Other Sins I & II",
    "Money Lending and Other Sins III", "The Spines of America",
    "Pouring Forth Oil (I & II)", "Pouring Forth Oil III & IV",
    "A Fisher of Men", "An American Pastoral Scene",
    "The Sheep and the Goats", "A Strange Kindness",
    "The New South", "Further Questions of Female Suffrage",
    "Money Lending and Other Sins IV", "American Distillation",
    "The Course of True Love I & II", "The Course of True Love III",
    "Advertising, the New American Art (I & II)", "Horse Flesh for Dinner",
    "The Fine Joys of Tobacco", "Magicians for Sport",
    "Friends in Very Low Places", "An Honest Mistake",
    "Preaching Forgiveness As He Went", "Sodom? Back to Gomorrah",
    "Blessed are the Peacemakers", "A Short Walk in a Pretty Town",
    "Blood Feuds, Ancient and Modern", "The Battle of Shady Belle",
    "The Joys of Civilization", "Angelo Bronte, a Man of Honor",
    "Money Lending and Other Sins V", "Help a Brother Out",
    "Brothers and Sisters, One and All", "Fatherhood and Other Dreams (I & II)",
    "No, No and Thrice, No", "The Gilded Cage",
    "A Fine Night of Debauchery", "American Fathers (I & II)",
    "High and Low Finance", "Horsemen, Apocalypses",
    "Urban Pleasures", "Country Pursuits",
    "Revenge is a Dish Best Eaten", "Banking, the Old American Art",
    "Welcome to the New World", "Savagery Unleashed",
    "A Kind and Benevolent Despot", "Hell Hath No Fury",
    "Paradise Mercifully Departed", "Dear Uncle Tacitus",
    "Fleeting Joy", "A Fork in the Road", "That's Murfree Country",
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
    "The Wheel", "Simple Pleasures", "Farming, for Beginners",
    "Fatherhood, for Beginners", "Old Habits",
    "Jim Milton Rides, Again?", "Fatherhood, for Idiots",
    "Motherhood", "Gainful Employment",
    "The Landowning Classes / Home of the Gentry?",
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
        "client_id": "1329870933695135785",
        "title_id":  "gta5_gen9",
        "large_image_story": "gta5_enhanced",
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
        "client_id": "356876176465199104",
        "title_id":  "gta5",
        "large_image_story": "gta5",
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
        "client_id": "643897785271189524",
        "title_id":  "rdr2",
        "large_image_story": "rdr2",
        "large_image_online": "rdr2_online",
        "details_story": "Playing Red Dead Redemption 2",
        "details_online": "Playing Red Dead Online",
        "missions": RDR2_STORY_MISSIONS,
        "activities": RDR2_ONLINE_ACTIVITIES,
        "max_players": 32,
        "color":     RED,
    },
}

ORDER = ["enhanced", "legacy", "rdr2"]


# ---------------------------------------------------------------
# Realistic Mission Duration Engine
# ---------------------------------------------------------------
# Based on community-reported data:
#   GTA V missions: 10-20 min average, 25-40 min for heists/finales
#   RDR2 missions: 20-45 min average, 45-60+ min for epics
#   GTA Online heists: 15-60 min depending on finale

def get_mission_duration(mission_name: str, game: str, index: int = 0,
                         total_missions: int = 0) -> int:
    """
    Return a realistic duration in seconds for a given mission.

    Uses keyword tiers plus chapter-based scaling so late-game missions
    feel longer, then adds slight random variance.
    """
    name = mission_name.lower().strip()

    # ── TIER 0: Ultra-short setups / chores / tutorials ─────────
    ultra_short = [
        "prologue", "chop", "casing", "carbine", "bugstars",
        "gas", "masks", "driller", "surveying", "wheel",
        "simple pleasures", "tools", "bad day",
        "fatherhood, for beginners", "pulling", "street race",
        "rampage", "grass roots", "pistol", "smg", "rifles",
        "shotguns", "heavy", "shooting range", "security van",
    ]
    if any(k in name for k in ultra_short):
        return random.randint(180, 420)      # 3–7 min

    # ── TIER 1: Short missions / quick story beats ──────────────
    short = [
        "father/son", "marriage counseling", "daddy's little girl",
        "friend request", "the good husband", "repossession",
        "complications", "franklin and lamar", "paparazzo",
        "bail bonds", "omega", "tennis", "yoga",
        "polite society", "americans at rest", "who is not without sin",
        "paying a social call", "a quiet time", "good, honest, snake oil",
        "the spines of america", "a fisher of men",
        "further questions of female suffrage", "american distillation",
        "the course of true love i & ii", "the course of true love iii",
        "help a brother out", "no, no and thrice, no",
        "do not seek absolution i", "do not seek absolution ii",
        "visiting hours", "just a social call", "motherhood",
        "gainful employment", "trying again", "uncle's bad day",
    ]
    if any(k in name for k in short):
        return random.randint(360, 720)      # 6–12 min

    # ── TIER 2: Epic heists / finales / multi-part missions ─────
    epic = [
        "jewel store job", "merryweather heist", "paleto score",
        "bureau raid", "big score", "third way", "ending a",
        "ending b", "ending c", "banking, the old american art",
        "blood feuds, ancient and modern", "red dead redemption",
        "american venom", "the battle of shady belle",
        "a short walk in a pretty town", "my last boy",
        "our best selves", "favored sons", "the king's son",
        "revenge is a dish best eaten",
    ]
    if any(k in name for k in epic):
        return random.randint(1500, 2700)    # 25–45 min

    # ── TIER 3: Long story missions / major set-pieces ──────────
    long_missions = [
        "mr. philips", "nervous ron", "crystal maze",
        "friends reunited", "fame or shame", "dead man walking",
        "three's company", "by the book", "hood safari",
        "scouting the port", "minisub", "cargobob",
        "the hotel assassination", "blitz play", "eye in the sky",
        "caida libre", "deep inside", "minor turbulence",
        "predator", "military hardware", "derailed",
        "monkey business", "hang ten", "bury the hatchet",
        "pack man", "fresh meat", "cleaning out the bureau",
        "the wrap up", "reuniting the family", "legal trouble",
        "lamar down", "meltdown", "parenting 101",
        "planning the big score", "the long stretch",
        "the first shall be last", "blessed are the meek?",
        "we loved once and true", "money lending and other sins",
        "pouring forth oil", "an american pastoral scene",
        "the sheep and the goats", "a strange kindness",
        "the new south", "advertising, the new american art",
        "horse flesh for dinner", "the fine joys of tobacco",
        "magicians for sport", "friends in very low places",
        "an honest mistake", "preaching forgiveness as he went",
        "sodom? back to gomorrah", "blessed are the peacemakers",
        "the joys of civilization", "angelo bronte, a man of honor",
        "brothers and sisters, one and all",
        "fatherhood and other dreams", "the gilded cage",
        "a fine night of debauchery", "american fathers",
        "high and low finance", "horsemen, apocalypses",
        "urban pleasures", "country pursuits",
        "welcome to the new world", "savagery unleashed",
        "a kind and benevolent despot", "hell hath no fury",
        "paradise mercifully departed", "dear uncle tacitus",
        "fleeting joy", "a fork in the road", "that's murfree country",
        "icarus and friends", "of men and angels",
        "the course of true love iv & v",
        "the delights of van horn", "the bridge to nowhere",
        "a rage unleashed", "archaeology for beginners",
        "honor, amongst thieves",
        "the fine art of conversation", "goodbye, dear friend",
        "mrs. sadie adler, widow", "jim milton rides, again?",
        "fatherhood, for idiots", "the landowning classes",
        "bare knuckles friendships",
        "home improvement for beginners", "an honest day's labors",
        "the tool box", "a new jerusalem",
        "a quick favor for an old friend",
        "a really big bastard", "a new future imagined",
    ]
    if any(k in name for k in long_missions):
        return random.randint(900, 1500)     # 15–25 min

    # ── TIER 4: Standard mission (default) ──────────────────────
    base_min, base_max = 600, 1200           # 10–20 min

    # Scale up slightly toward the end of the game (final act feel)
    if total_missions > 0 and index > 0:
        progress = index / total_missions
        if progress > 0.6:
            base_min = int(base_min * 1.2)
            base_max = int(base_max * 1.3)
        if progress > 0.85:
            base_min = int(base_min * 1.15)
            base_max = int(base_max * 1.2)

    return random.randint(base_min, base_max)


def get_online_activity_duration(activity: str) -> int:
    """Realistic duration for GTA Online / RDR Online activities."""
    a = activity.lower()

    if any(k in a for k in ["heist", "finale", "cayo", "doomsday",
                            "diamond", "casino"]):
        return random.randint(900, 3600)     # 15–60 min

    if any(k in a for k in ["bounty", "trading", "selling", "business",
                            "mission", "survival", "deathmatch"]):
        return random.randint(300, 900)      # 5–15 min

    if any(k in a for k in ["racing", "freemode", "hunting", "fishing",
                            "camping", "moseying"]):
        return random.randint(180, 600)      # 3–10 min

    return random.randint(300, 900)          # default 5–15 min


# ---------------------------------------------------------------
# Mission matching helper
# ---------------------------------------------------------------
def find_mission(missions, query: str):
    if not query:
        return None
    q = query.strip().lower()
    for m in missions:
        if m.lower() == q:
            return m
    pref = [m for m in missions if m.lower().startswith(q)]
    if len(pref) == 1:
        return pref[0]
    subs = [m for m in missions if q in m.lower()]
    if len(subs) == 1:
        return subs[0]
    if subs:
        return subs[0]
    return None


# ---------------------------------------------------------------
# RPC session wrapper (with auto-reconnect)
# ---------------------------------------------------------------
class RPCSession:
    RECONNECT_BASE = 5.0
    RECONNECT_MAX  = 60.0

    def __init__(self, game: str, mode: str = "online",
                 start_mission: str = None, heist_players: int = None):
        if game not in GAMES:
            raise ValueError(f"Unknown game: {game}")
        self.game = game
        self.mode = mode
        self.info = GAMES[game]
        self.presence = None
        self.connected = False

        self.start_ts = int(time.time())
        self.max_players = self.info["max_players"]
        self.heist_players = heist_players

        self.session_players = 0
        self.is_loading = (self.mode == "online")
        self.loading_target = random.randint(12, 24)
        self.last_update = time.time()

        self.missions = self.info["missions"]
        if start_mission:
            idx = self.missions.index(start_mission) if start_mission in self.missions else None
            if idx is None:
                resolved = find_mission(self.missions, start_mission)
                idx = self.missions.index(resolved) if resolved else 0
            self.mission_index = idx
        else:
            self.mission_index = 0

        self.mission_start_time = time.time()
        # Realistic duration via the duration engine
        self.mission_duration = get_mission_duration(
            self.missions[self.mission_index],
            self.game,
            self.mission_index,
            len(self.missions)
        )
        self.current_activity = (random.choice(self.info["activities"])
                                 if self.mode == "online" else None)
        self.activity_start_time = time.time()
        self.activity_duration = (
            get_online_activity_duration(self.current_activity)
            if self.current_activity else 600
        )

        self.reconnect_delay = self.RECONNECT_BASE
        self.next_reconnect_attempt = 0.0
        self.last_error = None

    # ---------------------------------------------------------
    # Status line
    # ---------------------------------------------------------
    def _log(self, msg: str):
        sys.stdout.write("\r\033[2K")
        sys.stdout.flush()
        print(msg)

    def _short_mission(self, name: str, width: int = 34) -> str:
        return name if len(name) <= width else name[: width - 3] + "..."

    def print_status(self):
        elapsed = int(time.time()) - self.start_ts
        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        elapsed_str = f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

        if self.connected:
            badge = c(" ● LIVE ", BOLD, GREEN)
        else:
            badge = c(" ○ WAIT ", BOLD, YELLOW)

        if self.mode == "story":
            mission = self._short_mission(self.missions[self.mission_index])
            remaining = max(0, int(self.mission_duration -
                                    (time.time() - self.mission_start_time)))
            rm, rs = divmod(remaining, 60)
            mid = (f"{c('Story', DIM, GRAY)} │ "
                   f"{c(mission, self.info['color'])} │ "
                   f"{c(f'next in {rm:02d}:{rs:02d}', DIM, GRAY)}")
        else:
            if self.heist_players is not None:
                mid = (f"{c('Heist', DIM, GRAY)} │ "
                       f"{c(f'{self.heist_players}/4 players', self.info['color'])}")
            else:
                act = self.current_activity or "Freemode"
                mid = (f"{c('Online', DIM, GRAY)} │ "
                       f"{c(act, self.info['color'])} │ "
                       f"{c(f'{self.session_players}/{self.max_players}', DIM, GRAY)}")

        line = (f"  {badge}  "
                f"{c(self.info['short'], BOLD, self.info['color'])} │ "
                f"{mid} │ "
                f"{c(elapsed_str, DIM, WHITE)}")
        sys.stdout.write("\r\033[2K" + line)
        sys.stdout.flush()

    # ---------------------------------------------------------
    # Simulation
    # ---------------------------------------------------------
    def _fluctuate_session(self):
        if self.mode == "story":
            return
        now = time.time()
        if now - self.last_update < 5:
            return
        self.last_update = now

        if self.is_loading:
            self.session_players += random.randint(1, 4)
            if self.session_players >= self.loading_target:
                self.is_loading = False
                self.session_players = random.randint(15, self.max_players - 2)
        else:
            if random.random() < 0.3:
                return
            change = random.randint(-3, 3)
            self.session_players = max(1, min(self.max_players,
                                              self.session_players + change))

    def _update_story_mission(self):
        """Advance the story mission once its simulated duration elapses.
        Uses the duration engine for realistic next-mission timing."""
        if self.mode != "story":
            return
        now = time.time()
        if now - self.mission_start_time > self.mission_duration:
            self.mission_index = (self.mission_index + 1) % len(self.missions)
            self.mission_start_time = now
            # Realistic duration for the NEW mission
            self.mission_duration = get_mission_duration(
                self.missions[self.mission_index],
                self.game,
                self.mission_index,
                len(self.missions)
            )

    def _update_online_activity(self):
        """Rotate online activities realistically over time."""
        if self.mode != "online" or self.heist_players is not None:
            return
        now = time.time()
        if now - self.activity_start_time > self.activity_duration:
            self.current_activity = random.choice(self.info["activities"])
            self.activity_start_time = now
            self.activity_duration = get_online_activity_duration(
                self.current_activity
            )

    def _update_state(self):
        self._fluctuate_session()
        self._update_story_mission()
        self._update_online_activity()

    # ---------------------------------------------------------
    # Presence I/O
    # ---------------------------------------------------------
    def _build_activity(self):
        if self.mode == "story":
            details = self.info["details_story"]
            state = self.missions[self.mission_index]
            large_image = self.info["large_image_story"]
        else:
            details = self.info["details_online"]
            if self.heist_players is not None:
                state = f"Heist ({self.heist_players} of 4)"
            else:
                if self.game in ("enhanced", "legacy"):
                    if random.random() < 0.5:
                        state = f"GTA Online ({self.session_players} of {self.max_players})"
                    else:
                        state = self.current_activity
                else:
                    state = f"Red Dead Online ({self.session_players} of {self.max_players})"
                    if random.random() < 0.5:
                        state = self.current_activity
            large_image = self.info["large_image_online"]

        buttons = [
            {"label": "Ask to Join", "url": "https://discord.com"},
            {"label": "Get on Steam", "url": "https://store.steampowered.com"},
        ]
        return dict(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            start=self.start_ts,
            large_image=large_image,
            large_text=self.info["label"],
            buttons=buttons,
        )

    def _push_activity(self):
        self.presence.update(**self._build_activity())

    def _push(self):
        self._update_state()
        self._push_activity()

    # ---------------------------------------------------------
    # Connection / reconnection
    # ---------------------------------------------------------
    def _open(self) -> bool:
        try:
            self.presence = Presence(self.info["client_id"])
            self.presence.connect()
            self.connected = True
            self.reconnect_delay = self.RECONNECT_BASE
            self.last_error = None
            self._push()
            return True
        except Exception as e:
            self.last_error = e
            self.connected = False
            if self.presence is not None:
                try:
                    self.presence.close()
                except Exception:
                    pass
            self.presence = None
            return False

    def connect(self):
        info = self.info
        mode_str = "Online" if self.mode == "online" else "Story"
        print(c("  ▶ ", info["color"]) +
              c(info["label"], BOLD, info["color"]) +
              c(f"  ({mode_str})", DIM, GRAY))
        print(c(f"    client_id={info['client_id']}  "
                f"title_id={info['title_id']}", DIM, GRAY))

        if self._open():
            print(c("    ✓ connected to Discord IPC", GREEN))
            return True

        print(c(f"    ✗ could not reach Discord IPC: {self.last_error}", YELLOW))
        print(c("      → is the Discord desktop app running?", GRAY))
        print(c("      → I'll keep retrying in the background…", GRAY))
        self.next_reconnect_attempt = time.time() + self.reconnect_delay
        return False

    def _handle_disconnect(self, e):
        self._log(c(f"  ⚠ Connection lost: {e}", YELLOW))
        self._log(c("    ↻ Waiting for Discord to come back…", GRAY))
        self.connected = False
        if self.presence is not None:
            try:
                self.presence.close()
            except Exception:
                pass
        self.presence = None
        self.last_error = e
        self.reconnect_delay = self.RECONNECT_BASE
        self.next_reconnect_attempt = time.time() + self.reconnect_delay

    def _try_reconnect(self):
        now = time.time()
        if now < self.next_reconnect_attempt:
            return
        if self._open():
            self._log(c("  ✓ Reconnected — presence restored.", BOLD, GREEN))
        else:
            self.reconnect_delay = min(self.reconnect_delay * 2,
                                       self.RECONNECT_MAX)
            self.next_reconnect_attempt = time.time() + self.reconnect_delay

    # ---------------------------------------------------------
    # Keepalive
    # ---------------------------------------------------------
    def keepalive(self):
        self._update_state()
        if self.connected and self.presence is not None:
            try:
                self._push_activity()
            except Exception as e:
                self._handle_disconnect(e)
        else:
            self._try_reconnect()

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------
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
        self.connected = False
        self._log(c("  ✕ presence cleared.", DIM, GRAY))


# ---------------------------------------------------------------
# Runners
# ---------------------------------------------------------------
KEEPALIVE_INTERVAL = 15


def run_single(game: str, mode: str = "online",
               start_mission: str = None, heist_players: int = None):
    info = GAMES[game]
    session = RPCSession(game, mode, start_mission, heist_players)
    session.connect()

    mode_str = "Online" if mode == "online" else "Story"
    print(c("  ▶ Presence armed: ", GRAY) +
          c(info["short"], BOLD, info["color"]) +
          c(f" ({mode_str})", DIM, GRAY) +
          c("   •   Ctrl+C to stop", GRAY))
    print()

    try:
        while True:
            time.sleep(KEEPALIVE_INTERVAL)
            session.keepalive()
            session.print_status()
    except KeyboardInterrupt:
        print()
    finally:
        session.close()


def run_cycle(games, interval: int, modes: dict, missions: dict, heist_map: dict):
    joined = c(" ↔ ", GRAY).join(
        c(GAMES[g]["short"], BOLD, GAMES[g]["color"]) for g in games
    )
    print(c(f"  ⇄ Cycling between {joined} ", GRAY) +
          c(f"every {interval}s.", GRAY))
    print(c("    Ctrl+C to stop and go back to the menu.", GRAY))
    print()

    current = None
    try:
        while True:
            for game in games:
                if current is not None:
                    print()
                    current.close()
                current = RPCSession(game, modes[game],
                                     missions.get(game),
                                     heist_map.get(game))
                current.connect()

                end = time.time() + interval
                while time.time() < end:
                    sleep_for = max(0.2, min(KEEPALIVE_INTERVAL,
                                             end - time.time()))
                    time.sleep(sleep_for)
                    current.keepalive()
                    current.print_status()
    except KeyboardInterrupt:
        print()
    finally:
        if current is not None:
            current.close()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
def show_menu():
    w = term_width()
    print()
    print(hrule("━", GRAY, w))
    print(c("  DISCORD RICH PRESENCE", BOLD, WHITE) + c("   │   ", GRAY) +
          c("GTA V", BOLD, GREEN) + c(" / ", GRAY) + c("RDR2", BOLD, RED))
    print(hrule("━", GRAY, w))

    for i, key in enumerate(ORDER, 1):
        info = GAMES[key]
        label = info["label"].ljust(38)
        print(f"   {c(str(i), BOLD, YELLOW)})  "
              f"{c(label, info['color'])} "
              f"{c('(' + info['title_id'] + ')', DIM, GRAY)}")

    print(f"   {c('4', BOLD, YELLOW)})  "
          f"{c('Cycle between TWO games...', WHITE)}")
    print(f"   {c('q', BOLD, YELLOW)})  {c('Quit', WHITE)}")
    print(hrule("━", GRAY, w))
    return input(c("  Choice: ", BOLD, WHITE)).strip().lower()


def _print_missions(missions, color):
    n = len(missions)
    half = (n + 1) // 2
    for i in range(half):
        left = f"{i + 1:>3}. {missions[i]}"
        line = "   " + c(left[:46].ljust(46), color)
        j = i + half
        if j < n:
            right = f"{j + 1:>3}. {missions[j]}"
            line += "  " + c(right[:46].ljust(46), color)
        print(line)


def _pick_mission_interactive(info):
    print()
    print(c("  ┌─ Story start point ─────────────────────────────", GRAY))
    print(f"   {c('1', BOLD, YELLOW)}) Start from the beginning "
          f"({c(info['missions'][0], info['color'])})")
    print(f"   {c('2', BOLD, YELLOW)}) Pick a mission by number")
    print(f"   {c('3', BOLD, YELLOW)}) Search missions by name")
    print(c("  └─────────────────────────────────────────────────", GRAY))
    sub = input(c("  Choice [1]: ", BOLD, WHITE)).strip() or "1"

    if sub == "1":
        return info["missions"][0], 0

    if sub == "3":
        q = input(c("  Search: ", BOLD, WHITE)).strip()
        if not q:
            return info["missions"][0], 0
        q_l = q.lower()
        matches = [(i, m) for i, m in enumerate(info["missions"])
                   if q_l in m.lower()]
        if not matches:
            print(c(f"  [!] No missions matching '{q}'. Starting from beginning.", RED))
            return info["missions"][0], 0
        print()
        for i, m in matches[:30]:
            print(f"   {c(str(i + 1), BOLD, YELLOW)})  {c(m, info['color'])}")
        if len(matches) > 30:
            print(c(f"   …and {len(matches) - 30} more", DIM, GRAY))
        raw = input(c("  Enter mission number (or Enter to abort): ", BOLD, WHITE)).strip()
        if not raw.isdigit():
            print(c("  [!] Aborted. Starting from beginning.", GRAY))
            return info["missions"][0], 0
        idx = int(raw) - 1
        if 0 <= idx < len(info["missions"]):
            return info["missions"][idx], idx
        print(c("  [!] Invalid. Starting from beginning.", RED))
        return info["missions"][0], 0

    print()
    print(c(f"  Missions for {info['short']}:", BOLD, info["color"]))
    _print_missions(info["missions"], info["color"])
    print()
    try:
        m_choice = int(input(c("  Enter mission number: ", BOLD, WHITE)).strip())
        if 1 <= m_choice <= len(info["missions"]):
            return info["missions"][m_choice - 1], m_choice - 1
    except ValueError:
        pass
    print(c("  [!] Invalid choice. Starting from the beginning.", RED))
    return info["missions"][0], 0


def ask_mode(game_key):
    info = GAMES[game_key]
    print()
    print(c("  Selected: ", GRAY) + c(info["short"], BOLD, info["color"]))
    print(f"   {c('1', BOLD, YELLOW)}) Story Mode")
    print(f"   {c('2', BOLD, YELLOW)}) Online Mode "
          f"{c('(realistic session loading)', DIM, GRAY)}")
    choice = input(c("  Choice [2]: ", BOLD, WHITE)).strip() or "2"

    if choice == "1":
        mission, _ = _pick_mission_interactive(info)
        return "story", mission, None

    heist_players = None
    if game_key in ("enhanced", "legacy"):
        print()
        print(c("  Simulate a Heist?", BOLD, WHITE))
        print(f"   {c('1', BOLD, YELLOW)}) Yes — pick player count")
        print(f"   {c('2', BOLD, YELLOW)}) No  — regular Online")
        hc = input(c("  Choice [2]: ", BOLD, WHITE)).strip() or "2"
        if hc == "1":
            raw = input(c("  How many players? 1-4  (Enter for random): ", GRAY)).strip()
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
        print(f"   {c(str(i), BOLD, info['color'])}) {c(info['label'], info['color'])}")
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
                modes, missions, heist_map = {}, {}, {}
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
        help="Story Mode starting mission (name or unique fragment)",
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

    resolved_mission = args.mission
    if (resolved_mission and args.mode in GAMES
            and args.type == "story"):
        found = find_mission(GAMES[args.mode]["missions"], resolved_mission)
        if not found:
            print(c(f"[!] Mission '{resolved_mission}' not found. "
                    f"Starting from the beginning.", YELLOW))
            resolved_mission = None
        else:
            print(c(f"[i] Starting from: ", GRAY) +
                  c(found, BOLD, GAMES[args.mode]["color"]))

    try:
        if args.mode == "menu":
            interactive()
        elif args.mode == "both":
            games = args.games or ["enhanced", "legacy"]
            modes = {g: args.type for g in games}
            missions = {}
            for g in games:
                m = args.mission
                if m and args.type == "story":
                    m = find_mission(GAMES[g]["missions"], m)
                missions[g] = m
            heist_map = {g: args.heist for g in games}
            run_cycle(games, args.interval, modes, missions, heist_map)
        else:
            run_single(args.mode, args.type, resolved_mission, args.heist)
    except KeyboardInterrupt:
        print(c("\n[*] Interrupted.", GRAY))
    except Exception as e:
        print(c(f"\n[!] Fatal: {e}", RED))
        sys.exit(1)


if __name__ == "__main__":
    main()
