"""
Versi non-interaktif dari test_post.py, dipanggil otomatis oleh GitHub Actions
sesuai jadwal di .github/workflows/threads-post.yml.
Generate 1 caption -> langsung posting -> log ke stdout (kelihatan di tab Actions).
"""
import os

from caption_generator import generate_caption
from threads_client import post_text

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]


def main():
    caption = generate_caption(ANTHROPIC_KEY)
    print(f"Caption: {caption}")
    post_id = post_text(USER_ID, ACCESS_TOKEN, caption)
    print(f"Berhasil posting. Post ID: {post_id}")


if __name__ == "__main__":
    main()
