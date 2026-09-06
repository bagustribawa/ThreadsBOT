"""
Post ke Threads berdasarkan content_calendar.json (sudah di-generate sebelumnya).
TIDAK memanggil API AI apa pun -- 100% gratis, tinggal ambil caption yang sudah
disiapkan sesuai tanggal & jam sekarang (waktu WITA).
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

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]

SLOTS = ["08:00", "12:30", "19:00", "21:30"]
TOLERANCE_MINUTES = 25  # toleransi keterlambatan GitHub Actions cron


def load_calendar():
    with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def closest_slot(now_hhmm: str):
    """Cari slot terdekat dari SLOTS, dalam toleransi TOLERANCE_MINUTES."""
    now_minutes = int(now_hhmm[:2]) * 60 + int(now_hhmm[3:])
    best_slot = None
    best_diff = None
    for slot in SLOTS:
        slot_minutes = int(slot[:2]) * 60 + int(slot[3:])
        diff = abs(now_minutes - slot_minutes)
        if best_diff is None or diff < best_diff:
            best_diff = diff
            best_slot = slot
    if best_diff is not None and best_diff <= TOLERANCE_MINUTES:
        return best_slot
    return None


def main():
    now_wita = datetime.datetime.now(ZoneInfo("Asia/Makassar"))
    today_str = now_wita.date().isoformat()
    now_hhmm = now_wita.strftime("%H:%M")

    slot = closest_slot(now_hhmm)
    if slot is None:
        print(f"Jam sekarang ({now_hhmm} WITA) tidak dekat slot manapun, skip.")
        return

    calendar = load_calendar()
    match = next((e for e in calendar if e["date"] == today_str and e["slot"] == slot), None)

    if match is None:
        print(f"Tidak ada entry untuk {today_str} slot {slot} di content_calendar.json. "
              f"Kalender mungkin sudah habis -- perlu di-generate ulang untuk bulan berikutnya.")
        return

    caption = match["caption"]
    print(f"Posting untuk {today_str} slot {slot}: {caption}")
    post_id = post_text(USER_ID, ACCESS_TOKEN, caption)
    print(f"Berhasil posting. Post ID: {post_id}")


if __name__ == "__main__":
    main()
