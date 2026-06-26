```markdown
# WorkFest — Scraper de festivals de musique France 2026

Projet CI/CD qui scrape automatiquement les sites officiels de 34 festivals de musique français pour générer des notes Obsidian structurées, le tout orchestré via GitHub Actions et Docker.

## Structure du projet

```
WorkFest/
├── main.py                   
├── requirements.txt          
├── config/
│   ├── settings.py           
│   └── festivals.py          
├── Scraper/
│   ├── scraper.py            
│   ├── helpers.py            
│   └── dates.py              
├── notes/
│   ├── generator.py          
│   └── writers.py            
├── docker/
│   └── Dockerfile            
└── .github/workflows/
    └── festivals.yml         
```

## Dépendances

| Package | Version | Rôle |
| `requests` | 2.32.3 | Requêtes HTTP vers les sites |
| `beautifulsoup4` | 4.12.3 | Parsing HTML |
| `lxml` | 5.2.2 | Parser HTML rapide pour BeautifulSoup |

## Prérequis — installation depuis zéro

### Python (si pas installé)

Télécharge Python sur **https://python.org/downloads**  
⚠️ Coche **"Add Python to PATH"** pendant l'installation.

Vérifie ensuite :

```powershell
python --version
pip --version
```

### Git (si pas installé)

Télécharge sur **https://git-scm.com/downloads** et installe avec les options par défaut.

## Installation et lancement

### En local (sans Docker)

```bash
# Cloner le projet
git clone https://github.com/CS2I-P20-Antoine-LIDURIN/WorkFest.git
cd WorkFest

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le scraper
python main.py
```

Les notes sont générées dans le dossier `output/` par défaut.

### Avec Docker (sans installer Python)

```bash
# Construire l'image
docker build -t festivals-scraper -f docker/Dockerfile .

# Lancer le scraper (les notes sont dans ./output/)
mkdir -p output
docker run --rm \
  -e OUTPUT_DIR=/output \
  -v $(pwd)/output:/output \
  festivals-scraper
```

Sur Windows (PowerShell) :

```powershell
docker build -t festivals-scraper -f docker/Dockerfile .
mkdir output
docker run --rm -e OUTPUT_DIR=/output -v ${PWD}/output:/output festivals-scraper
```

### Via GitHub Actions

Le workflow se déclenche automatiquement à chaque push sur `main`.  
Il peut aussi être lancé manuellement depuis l'onglet **Actions** → **Festivals 2026 - Scraper** → **Run workflow**.

Les notes générées sont disponibles en téléchargement dans les **Artifacts** du run sous le nom `festivals-obsidian-2026`.

## Résultat

Le scraper génère dans `output/` :

```
output/
├── INDEX.md                  
├── 2026-06-Juin.md          
├── 2026-07-Juillet.md
├── ...
├── 2026-00-Sans-date.md      
└── festivals/
    ├── Hellfest.md           
    ├── Rock en Seine.md
    └── ...
```

