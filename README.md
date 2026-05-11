# FON Katedra Monitor 🔔

Automatski prati https://is.fon.bg.ac.rs/ i šalje ntfy notifikaciju kada se pojavi novi post.  
Radi besplatno na GitHub Actions — ne treba ti uključen kompjuter ni server.

## Setup (5 minuta)

### 1. Napravi GitHub repo

- Idi na github.com → New repository
- Ime: `fon-monitor` (može biti private)
- Upload-uj oba fajla: `fon_monitor.py` i `.github/workflows/monitor.yml`

### 2. Dodaj NTFY_TOPIC Secret

- U repozitorijumu: **Settings → Secrets and variables → Actions → New repository secret**
- Name: `NTFY_TOPIC`
- Value: tvoj jedinstven topic (npr. `nikola-fon-xyz123`)

### 3. Pretplati se na ntfy

- Skini ntfy app na telefon
- Tap **Subscribe to topic** → upiši isti topic

### 4. Omogući Actions

- Idi na **Actions** tab u repou
- Ako piše "Workflows aren't running" → klikni Enable

### 5. Testiraj ručno

- Actions → **FON Monitor** → **Run workflow**
- Proveraš logove, treba da vidiš "Prvo pokretanje, pamtim postojeće postove..."
- Drugi ručni run → "Ništa novo." → sve radi ✓

---

Od sad radi automatski svakih 30 min. Kad katedra objavi nešto novo, stižeš notifikaciju.

## Napomene

- **GitHub Actions free tier**: 2000 min/mesec. Svaki run traje ~20s → ~480 min/mesec. Daleko ispod limita.
- **seen_posts.json** se automatski kreira i commit-uje u repo pri prvom pokretanju.
- Ako hoćeš češće provere, promeni `*/30` na `*/15` u workflow fajlu (minimum koji je pouzdan na GitHub Actions).
- GitHub Actions cron može kasniti do ~10 min — to je ok za ovu namenu.
# fon-monitor
