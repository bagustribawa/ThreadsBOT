"""
Post ke Threads berdasarkan content_calendar.json.
Didesain robust terhadap keterbatasan GitHub Actions:
- cron bisa delay atau di-drop saat load tinggi (didokumentasikan resmi oleh GitHub)
- makanya script ini dipanggil tiap 15 menit, dan window toleransi per slot
  cukup lebar (90 menit setelah jam target), plus ada state file (posted_log.json)
  supaya tidak posting dobel untuk slot yang sama.
"""
import json
import os
import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    from backports.zoneinfo import ZoneInfo

from threads_client import post_text

BASE_DIR = os.path.dirname(__file__)
CALENDAR_FILE = os.path.join(BASE_DIR, "content_calendar.json")
POSTED_LOG_FILE = os.path.join(BASE_DIR, "posted_log.json")

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]

SLOTS = ["08:00", "12:30", "19:00", "21:30"]
WINDOW_MINUTES_AFTER = 90  # toleransi: boleh posting sampai 90 menit setelah jam target


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def already_posted(posted_log, key: str) -> bool:
    return key in posted_log.get("done", [])


def mark_posted(posted_log, key: str):
    posted_log.setdefault("done", []).append(key)
    save_json(POSTED_LOG_FILE, posted_log)


def find_due_slot(now_wita: datetime.datetime, posted_log: dict):
    """
    Cari slot hari ini yang jamnya sudah lewat (dalam window toleransi)
    tapi belum ditandai sudah posting.
    """
    today_str = now_wita.date().isoformat()
    for slot in SLOTS:
        key = f"{today_str}_{slot}"
        if already_posted(posted_log, key):
            continue
        slot_dt = datetime.datetime.combine(
            now_wita.date(),
            datetime.time(int(slot[:2]), int(slot[3:])),
            tzinfo=now_wita.tzinfo,
        )
        minutes_since_slot = (now_wita - slot_dt).total_seconds() / 60
        if 0 <= minutes_since_slot <= WINDOW_MINUTES_AFTER:
            return slot, key, today_str
    return None, None, None


def main():
    now_wita = datetime.datetime.now(ZoneInfo("Asia/Makassar"))
    posted_log = load_json(POSTED_LOG_FILE, {"done": []})

    slot, key, today_str = find_due_slot(now_wita, posted_log)
    if slot is None:
        print(f"Jam sekarang {now_wita.strftime('%H:%M')} WITA -- tidak ada slot yang due, skip.")
        return

    calendar = load_json(CALENDAR_FILE, [])
    match = next((e for e in calendar if e["date"] == today_str and e["slot"] == slot), None)

    if match is None:
        print(f"Slot {slot} due tapi tidak ada entry di content_calendar.json untuk {today_str}. "
              f"Kemungkinan kalender sudah habis, perlu generate batch baru.")
        return

    caption = match["caption"]
    print(f"Posting untuk {today_str} slot {slot} (dieksekusi jam {now_wita.strftime('%H:%M')} WITA): {caption}")
    post_id = post_text(USER_ID, ACCESS_TOKEN, caption)
    print(f"Berhasil posting. Post ID: {post_id}")

    mark_posted(posted_log, key)


if __name__ == "__main__":
    main()
