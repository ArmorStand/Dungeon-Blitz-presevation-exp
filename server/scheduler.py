import glob
import json
import os
import threading
import time
import heapq
import struct

from BitBuffer import BitBuffer
from Character import save_characters, load_characters, CHAR_SAVE_DIR
from constants import class_111, class_64_const_218, class_1, class_66

# Will be set by server.py to resolve (user_id, char_name) → ClientSession
active_session_resolver = None

def set_active_session_resolver(fn):
    """
    fn(user_id: str, char_name: str) -> ClientSession or None
    """
    global active_session_resolver
    active_session_resolver = fn

class TaskScheduler:
    def __init__(self):
        self._lock = threading.Lock()
        self._queue = []  # heap of (run_at, id, callback)
        self._next_id = 0
        self._new_event = threading.Event()
        threading.Thread(target=self._run_loop, daemon=True).start()

    def schedule(self, run_at: int, callback: callable):
        with self._lock:
            heapq.heappush(self._queue, (run_at, self._next_id, callback))
            self._next_id += 1
            self._new_event.set()

    def _run_loop(self):
        while True:
            with self._lock:
                if not self._queue:
                    timeout = None
                else:
                    run_at, _, _ = self._queue[0]
                    timeout = max(0, run_at - int(time.time()))
            self._new_event.wait(timeout=timeout)
            self._new_event.clear()

            now = int(time.time())
            to_run = []
            with self._lock:
                while self._queue and self._queue[0][0] <= now:
                    _, _, cb = heapq.heappop(self._queue)
                    to_run.append(cb)
            for cb in to_run:
                try:
                    cb()
                except Exception as e:
                    print(f"[Scheduler] callback error: {e}")

# singleton instance
scheduler = TaskScheduler()

def reschedule_for_session(session):
    now = int(time.time())
    for char in session.char_list:
        research = char.get("research")
        if not research:
            continue

        ready_ts = research.get("ReadyTime", 0)
        is_done = research.get("done", False)

        if ready_ts <= now:
            if not is_done:
                research["done"] = True
                save_characters(session.user_id, session.char_list)
                print(f"[{session.addr}] Offline research marked done …")

                # Send the "research complete" packet immediately
                bb = BitBuffer()
                bb.write_method_6(research["abilityID"], 7)
                payload = bb.to_bytes()
                session.conn.sendall(struct.pack(">HH", 0xC0, len(payload)) + payload)
                print(f"[{session.addr}] Sent research-complete on login abilityID={research['abilityID']}")
        else:
            # Schedule callback for when it's due
            scheduler.schedule(
                run_at=ready_ts,
                callback=lambda uid=session.user_id, cname=char["name"]: _on_research_done_for(uid, cname)
            )

def _on_research_done_for(user_id: str, char_name: str):
    # Load persistent data
    chars = load_characters(user_id)
    char = next((c for c in chars if c.get("name") == char_name), None)
    if not char or "research" not in char:
        return
    research = char["research"]
    if research.get("done", False):
        return
    research["done"] = True
    save_characters(user_id, chars)

    # Update in‐memory and notify active session
    if active_session_resolver:
        session = active_session_resolver(user_id, char_name)
        if session and session.authenticated:
            mem_char = next((c for c in session.char_list if c.get("name") == char_name), None)
            if mem_char and "research" in mem_char:
                mem_char["research"]["done"] = True
            try:
                bb = BitBuffer()
                bb.write_method_6(research["abilityID"], 7)
                payload = bb.to_bytes()
                session.conn.sendall(struct.pack(">HH", 0xbf, len(payload)) + payload)
                print(f"[{session.addr}] Sent research-complete (0xbf) abilityID={research['abilityID']}")
            except Exception as e:
                print(f"[Scheduler] notify failed: {e}")

def schedule_research(user_id: str, char_name: str, ready_ts: int):
    handle = scheduler.schedule(
        run_at=ready_ts,
        callback=lambda uid=user_id, cn=char_name: _on_research_done_for(uid, cn)
    )
    return handle


def _on_building_done_for(user_id: str, char_name: str):
    chars = load_characters(user_id)
    char = next((c for c in chars if c.get("name") == char_name), None)
    if not char:
        return

    bu = char.get("buildingUpgrade", {})
    if not isinstance(bu, dict):
        return

    now = int(time.time())
    # Skip if canceled or not ready
    if bu.get("buildingID", 0) == 0:
        return
    if bu.get("done") or bu.get("ReadyTime", 0) > now:
        return

    building_id = bu.get("buildingID")
    new_rank    = bu.get("rank")

    bu["done"] = True
    mf = char.setdefault("magicForge", {})
    stats_dict = mf.setdefault("stats_by_building", {})
    if building_id and new_rank:
        stats_dict[str(building_id)] = new_rank

    # Clear state after completion
    char["buildingUpgrade"] = {
        "buildingID": 0,
        "rank": 0,
        "ReadyTime": 0,
        "done": False,
    }
    save_characters(user_id, chars)

    if not active_session_resolver:
        return
    session = active_session_resolver(user_id, char_name)
    if not (session and session.authenticated):
        return

    mem_char = next((c for c in session.char_list if c.get("name") == char_name), None)
    if mem_char:
        mem_mf = mem_char.setdefault("magicForge", {})
        mem_stats = mem_mf.setdefault("stats_by_building", {})
        if building_id and new_rank:
            mem_stats[str(building_id)] = new_rank
        mem_char["buildingUpgrade"] = char["buildingUpgrade"].copy()

    # Notify client (0xD8)
    try:
        bb = BitBuffer()
        bb.write_method_6(building_id, 5)
        bb.write_method_6(new_rank, 5)
        bb.write_method_15(True)  # status = complete
        payload = bb.to_bytes()
        session.conn.sendall(struct.pack(">HH", 0xD8, len(payload)) + payload)
        print(f"[{session.addr}] Sent building-complete (0xD8) ID={building_id}, rank={new_rank}")
    except Exception as e:
        print(f"[Scheduler] building notify failed: {e}")


def schedule_building_upgrade(user_id: str, char_name: str, ready_ts: int):
    handle = scheduler.schedule(
        run_at=ready_ts,
        callback=lambda uid=user_id, cn=char_name: _on_building_done_for(uid, cn)
    )

    # Store the scheduler ID so it can be canceled later
    chars = load_characters(user_id)
    char = next((c for c in chars if c.get("name") == char_name), None)
    if char:
        bu = char.setdefault("buildingUpgrade", {})
        bu["schedule_id"] = handle
        save_characters(user_id, chars)




def _on_forge_done_for(user_id: str, char_name: str, primary: int, secondary: int):
    # 1) Load persistent data
    chars = load_characters(user_id)
    char = next((c for c in chars if c.get("name") == char_name), None)
    if not char or "magicForge" not in char:
        return
    mf = char["magicForge"]

    # 2) Mark the forge session as completed
    mf["hasSession"] = False
    mf["status"]     = class_111.const_264   # your “completed” constant
    mf["duration"]   = 0

    save_characters(user_id, chars)

    # 3) If user is online, mirror and notify
    if active_session_resolver:
        session = active_session_resolver(user_id, char_name)
        if session and session.authenticated:
            # Mirror into live session
            mem_char = next((c for c in session.char_list if c.get("name") == char_name), None)
            if mem_char:
                mem_mf = mem_char.setdefault("magicForge", {})
                mem_mf.update({
                    "hasSession": False,
                    "status":    class_111.const_264,
                    "duration":  0,
                    "var_8":     1 if secondary else 0
                })

            # Build & send “forge complete” packet (0xCD or your chosen opcode)
            try:
                bb = BitBuffer()
                bb.write_method_6(primary,   class_1.const_254)
                bb.write_method_11(1 if secondary else 0, 1)
                if secondary:
                    bb.write_method_6(secondary, class_64_const_218)
                payload = bb.to_bytes()
                session.conn.sendall(struct.pack(">HH", 0xCD, len(payload)) + payload)
                print(f"[{session.addr}] Sent forge-complete packet")
            except Exception as e:
                print(f"[Scheduler] forge notify failed: {e}")

def schedule_forge(user_id: str, char_name: str, run_at: int, primary: int, secondary: int):
    scheduler.schedule(
        run_at=run_at,
        callback=lambda uid=user_id, cn=char_name, p=primary, s=secondary:
            _on_forge_done_for(uid, cn, p, s)
    )

def _on_talent_done_for(user_id: str, char_name: str):
    chars = load_characters(user_id)
    char = next((c for c in chars if c.get("name") == char_name), None)
    if not char:
        return

    tr = char.get("talentResearch", {})
    now = int(time.time())
    if tr.get("done") or tr.get("ReadyTime", 0) > now:
        return

    # 1) Mark research as done (but don’t award point yet)
    tr["done"] = True
    save_characters(user_id, chars)

    # 2) Update in-memory session if online
    if not active_session_resolver:
        return
    session = active_session_resolver(user_id, char_name)
    if not (session and session.authenticated):
        return

    mem_char = next((c for c in session.char_list if c.get("name") == char_name), None)
    if mem_char:
        mem_char["talentResearch"] = tr.copy()

    # 3) Notify client with 0xD5 “research complete”
    try:
        bb = BitBuffer()
        bb.write_method_6(tr.get("classIndex"), 2)  # classIndex
        bb.write_method_6(1, 1)                     # status = complete
        payload = bb.to_bytes()
        session.conn.sendall(struct.pack(">HH", 0xD5, len(payload)) + payload)
        print(f"[{session.addr}] Sent 0xD5 research complete for classIndex={tr.get('classIndex')}")
    except Exception as e:
        print(f"[Scheduler] talent notify failed: {e}")

def schedule_Talent_point_research(user_id: str, char_name: str, run_at: int):
    handle = scheduler.schedule(
        run_at=run_at,
        callback=lambda uid=user_id, cn=char_name: _on_talent_done_for(uid, cn)
    )
    return handle

def boot_scan_all_saves():
    now = int(time.time())
    for path in glob.glob(os.path.join(CHAR_SAVE_DIR, "*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        chars = data.get("characters", [])
        dirty = False

        for char in chars:
            # — Research (singular dict) —
            research = char.get("research")
            if research and not research.get("done", False):
                rt = research.get("ReadyTime", 0)
                if rt <= now:
                    research["done"] = True
                    dirty = True
                else:
                    schedule_research(char.get("user_id"), char["name"], rt)

            # — Building upgrades (allow dict or list) —
            bu = char.get("buildingUpgrade")
            entries = []
            if isinstance(bu, dict):
                entries = [bu]
            elif isinstance(bu, list):
                entries = bu

            for upgrade in entries:
                if not upgrade.get("done", False):
                    rt = upgrade.get("ReadyTime", 0)
                    if rt <= now:
                        upgrade["done"] = True
                        dirty = True
                    else:
                        schedule_building_upgrade(char.get("user_id"), char["name"], rt)

            # — Magic Forge sessions —
            mf = char.get("magicForge")
            # We only care if there’s an active session in‑progress
            if isinstance(mf, dict) and mf.get("hasSession") and mf.get("status") == class_111.const_286:
                start_ts = mf.get("_start_time", 0)
                duration_ms = mf.get("duration", 0)
                ready_ts = start_ts + (duration_ms // 1000)
                if ready_ts <= now:
                    # expired: mark done immediately
                    mf["hasSession"] = False
                    mf["status"]     = class_111.const_264  # completed
                    mf["duration"]   = 0
                    dirty = True
                else:
                    # not yet ready: schedule callback
                    schedule_forge(
                        char.get("user_id"),
                        char["name"],
                        ready_ts,
                        mf.get("primary", 0),
                        mf.get("secondary", 0)
                    )

            tr = char.get("talentResearch", {})
            if tr and not tr.get("done", False):
                rt = tr.get("ReadyTime", 0)
                if rt <= now:
                    # expired: mark done immediately
                    tr["done"] = True
                    dirty = True
                else:
                    # still pending: schedule its completion
                    schedule_Talent_point_research(
                        char.get("user_id"),
                        char["name"],
                        rt
                    )


        if dirty:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Boot‑scan: patched expired timers in {os.path.basename(path)}")

# Call once at import / server startup
boot_scan_all_saves()


