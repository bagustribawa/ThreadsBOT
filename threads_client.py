"""
Client kecil untuk posting ke Threads API (container -> publish pattern)
dan refresh long-lived access token sebelum expired.
"""
import time
import requests

GRAPH_URL = "https://graph.threads.net/v1.0"


def post_text(user_id: str, access_token: str, text: str) -> str:
    """Post teks ke Threads. Return ID post yang berhasil dibuat."""
    # Step 1: buat container
    container_resp = requests.post(
        f"{GRAPH_URL}/{user_id}/threads",
        params={
            "media_type": "TEXT",
            "text": text,
            "access_token": access_token,
        },
        timeout=30,
    )
    container_resp.raise_for_status()
    creation_id = container_resp.json()["id"]

    # Threads butuh sedikit delay sebelum container siap dipublish
    time.sleep(5)

    # Step 2: publish container
    publish_resp = requests.post(
        f"{GRAPH_URL}/{user_id}/threads_publish",
        params={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    publish_resp.raise_for_status()
    return publish_resp.json()["id"]


def refresh_long_lived_token(access_token: str) -> dict:
    """
    Refresh long-lived token Threads. Sebaiknya dipanggil tiap beberapa hari
    sekali (jauh sebelum expired di hari ke-60), token lama harus masih valid.
    Return dict berisi access_token baru & expires_in (detik).
    """
    resp = requests.get(
        f"{GRAPH_URL}/refresh_access_token",
        params={
            "grant_type": "th_refresh_token",
            "access_token": access_token,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
