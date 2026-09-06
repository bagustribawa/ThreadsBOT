"""
Generate satu caption Threads baru menggunakan Anthropic API,
berdasarkan topik & format acak dari topics.json.
"""
import json
import random
import os
import anthropic

TOPICS_FILE = os.path.join(os.path.dirname(__file__), "topics.json")


def load_topics():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_caption(api_key: str) -> str:
    data = load_topics()
    topic = random.choice(data["topics"])
    fmt = random.choice(data["formats"])
    gaya = data.get("gaya_bahasa", "santai dan natural")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Buatkan 1 post untuk Threads (mirip Twitter/X, max 500 karakter) dengan ketentuan:
- Topik: {topic}
- Format: {fmt}
- Gaya bahasa: {gaya}
- JANGAN pakai tanda kutip di awal/akhir.
- JANGAN pakai hashtag lebih dari 1 (boleh 0).
- Buat semenarik mungkin biar orang mau reply/like, tapi tetap terasa natural dan personal, bukan seperti iklan.
- Balas HANYA dengan teks captionnya saja, tanpa penjelasan tambahan.
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    caption = response.content[0].text.strip()
    # Safety net: pastikan tidak lewat limit karakter Threads
    if len(caption) > 500:
        caption = caption[:497] + "..."
    return caption


if __name__ == "__main__":
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise SystemExit("Set ANTHROPIC_API_KEY dulu di .env")
    print(generate_caption(key))
