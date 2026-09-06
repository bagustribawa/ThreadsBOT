# Setup Threads Auto-Poster via GitHub Actions (GRATIS, tanpa VPS)

Bot ini jalan otomatis di server GitHub sesuai jadwal — kamu tidak perlu nyalakan
laptop/HP, dan tidak perlu bayar VPS.

## Langkah-langkah

### 1. Buat akun GitHub (kalau belum punya)
Daftar gratis di https://github.com/signup

### 2. Buat repository baru
1. Klik tombol '+' di kanan atas → 'New repository'
2. Nama bebas, misal `threads-bot`
3. **Pilih 'Private'** (jangan Public — biar orang lain nggak lihat struktur bot kamu)
4. Klik 'Create repository'

### 3. Upload semua file bot ke repo ini
Struktur folder yang perlu di-upload persis seperti ini:
```
threads-bot/
├── .github/
│   └── workflows/
│       └── threads-post.yml
├── caption_generator.py
├── threads_client.py
├── post_once.py
├── topics.json
├── requirements.txt
```
Cara upload paling gampang (tanpa command line):
1. Di halaman repo GitHub, klik 'Add file' → 'Upload files'
2. Drag & drop semua file (KECUALI `.env`, `scheduler.py`, `test_post.py`,
   `schedule.json`, `threads-bot.service` — file-file itu tidak dipakai di jalur ini)
3. Untuk folder `.github/workflows/threads-post.yml`, kamu perlu upload dengan
   struktur foldernya tetap — GitHub web upload otomatis mendeteksi folder kalau
   kamu drag seluruh folder `.github` sekaligus dari file explorer komputer kamu
4. Klik 'Commit changes'

**PENTING**: JANGAN upload file `.env` ke GitHub — kredensialnya harus masuk lewat
'Secrets' (langkah berikutnya), bukan file biasa, meski repo-nya private.

### 4. Masukkan kredensial ke GitHub Secrets
1. Di repo, klik tab 'Settings'
2. Sidebar kiri: 'Secrets and variables' → 'Actions'
3. Klik 'New repository secret', buat 3 secret ini satu-satu:

| Name | Value |
|---|---|
| `THREADS_ACCESS_TOKEN` | token panjang dari Meta dashboard |
| `THREADS_USER_ID` | `38193604593617085` |
| `ANTHROPIC_API_KEY` | key dari console.anthropic.com |

### 5. Edit topics.json sesuai keinginan
Klik file `topics.json` di repo → ikon pensil (Edit) → ubah isi `topics` sesuai
niche kamu → 'Commit changes'.

### 6. Test jalan manual dulu
1. Klik tab 'Actions' di repo
2. Klik workflow 'Threads Auto Post' di sidebar kiri
3. Klik tombol 'Run workflow' (dropdown di kanan) → 'Run workflow' lagi untuk konfirmasi
4. Tunggu ~30 detik, refresh halaman → klik run yang baru muncul → lihat log-nya
5. Kalau sukses, cek langsung di app Threads kamu — harusnya ada post baru
6. Kalau ada error merah, klik untuk expand detail errornya, screenshot, kirim ke saya

### 7. Selesai — biarkan jalan otomatis
Setelah test berhasil, bot akan otomatis jalan sesuai jadwal di
`.github/workflows/threads-post.yml` (default: 4x sehari, jam WITA
08:00 / 12:30 / 19:00 / 21:30). Kamu bisa cek riwayat postingan kapan saja
di tab 'Actions'.

## Mengubah jadwal jam posting
Edit file `.github/workflows/threads-post.yml`, bagian `cron:`. Formatnya
`menit jam * * *` dalam **UTC**, bukan WITA. WITA = UTC+8, jadi kurangi 8 jam
dari jam WITA yang kamu mau. Setelah edit, commit — jadwal baru langsung aktif.

## Refresh token (tiap ~45-60 hari)
GitHub Actions tidak bisa refresh token otomatis untuk kamu. Reminder di kalender:
1. Buka Meta dashboard → generate access token baru (cara sama seperti sebelumnya)
2. Update value secret `THREADS_ACCESS_TOKEN` di GitHub (Settings → Secrets →
   klik nama secret → Update)

## Kalau mau berhenti sementara
Tab 'Actions' → klik workflow 'Threads Auto Post' → titik tiga (⋯) di kanan atas →
'Disable workflow'.
