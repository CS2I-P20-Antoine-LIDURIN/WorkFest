import os
import re
from datetime import datetime

from config.settings import OUTPUT_DIR, MONTHS_FR


def generate_notes(festivals):

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    notes_dir = os.path.join(OUTPUT_DIR, "festivals")
    os.makedirs(notes_dir, exist_ok=True)

    by_month = {}
    no_date = []

    for f in festivals:
        if f.get("month"):
            by_month.setdefault(f["month"], []).append(f)
        else:
            no_date.append(f)

    # ── Note individuelle par festival ──────────────────────────────────
    for f in festivals:
        safe_name = re.sub(r'[\\/*?:"<>|]', "-", f["name"])
        filepath = os.path.join(notes_dir, f"{safe_name}.md")

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(f"# {f['name']}\n\n")

            if f.get("statut") and f["statut"] != "ok":
                fh.write(f"> ⚠️ Site inaccessible : {f['statut']}\n\n")

            fh.write("## Informations\n\n")
            fh.write("| Champ | Valeur |\n")
            fh.write("|-------|--------|\n")
            fh.write(f"| 📍 Ville  | {f.get('ville', '')} |\n")
            fh.write(f"| 🎸 Genre  | {f.get('genre', '')} |\n")

            if f.get("dates_2026"):
                fh.write(f"| 📅 Dates  | {' · '.join(f['dates_2026'])} |\n")

            fh.write(f"| 🌐 Site   | [{f.get('url', '')}]({f.get('url', '')}) |\n")
            fh.write("\n")

            if f.get("description"):
                fh.write("## Description\n\n")
                fh.write(f"{f['description']}\n\n")

            if f.get("artistes"):
                fh.write("## Artistes\n\n")
                for artiste in f["artistes"]:
                    fh.write(f"- {artiste}\n")
                fh.write("\n")

            fh.write("---\n\n[[INDEX|← Retour à l'index]]\n")

    # ── Notes mensuelles ────────────────────────────────────────────────
    for month_num, events in sorted(by_month.items()):
        month_name = MONTHS_FR[month_num]
        filepath = os.path.join(OUTPUT_DIR, f"2026-{month_num:02d}-{month_name}.md")

        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(f"# 🎵 Festivals — {month_name} 2026\n\n")
            fh.write(f"> {len(events)} festival(s) · [[INDEX|← Index]]\n\n---\n\n")
            for evt in sorted(events, key=lambda x: x["name"]):
                safe = re.sub(r'[\\/*?:"<>|]', "-", evt["name"])
                fh.write(f"## [[festivals/{safe}|{evt['name']}]]\n\n")
                fh.write(f"- 📍 **{evt.get('ville', '')}** · 🎸 {evt.get('genre', '')}\n")
                if evt.get("dates_2026"):
                    fh.write(f"- 📅 {' · '.join(evt['dates_2026'][:2])}\n")
                if evt.get("description"):
                    desc = evt["description"][:200]
                    fh.write(f"\n> {desc}\n")
                fh.write("\n---\n\n")

    # ── Note sans date ───────────────────────────────────────────────────
    if no_date:
        filepath = os.path.join(OUTPUT_DIR, "2026-00-Sans-date.md")
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("# 🎵 Festivals — Date non trouvée\n\n")
            fh.write(f"> {len(no_date)} festival(s) · [[INDEX|← Index]]\n\n---\n\n")
            for f in sorted(no_date, key=lambda x: x["name"]):
                safe = re.sub(r'[\\/*?:"<>|]', "-", f["name"])
                fh.write(f"- [[festivals/{safe}|{f['name']}]] — {f.get('ville', '')}\n")

    # ── Index global ─────────────────────────────────────────────────────
    index_path = os.path.join(OUTPUT_DIR, "INDEX.md")
    total = len(festivals)
    confirmed = sum(1 for f in festivals if f.get("dates_2026"))

    with open(index_path, "w", encoding="utf-8") as fh:
        fh.write("# 🎵 Festivals de musique en France — 2026\n\n")
        fh.write(f"> Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}  \n")
        fh.write(f"> **{total} festivals** · **{confirmed} avec dates 2026 confirmées** ✅\n\n")
        fh.write("## 📅 Par mois\n\n")
        for month_num in sorted(by_month.keys()):
            name = MONTHS_FR[month_num]
            count = len(by_month[month_num])
            fh.write(f"- [[2026-{month_num:02d}-{name}]] — {count} festival(s)\n")
        if no_date:
            fh.write(f"- [[2026-00-Sans-date]] — {len(no_date)} sans date\n")
        fh.write("\n## 🗂️ Tous les festivals\n\n")
        for f in sorted(festivals, key=lambda x: x["name"]):
            safe = re.sub(r'[\\/*?:"<>|]', "-", f["name"])
            tick = " ✅" if f.get("dates_2026") else ""
            fh.write(f"- [[festivals/{safe}|{f['name']}]]{tick} — {f.get('ville', '')}\n")

    print(f"✅ {total} notes générées dans {OUTPUT_DIR}/")
    print(f"   {confirmed}/{total} avec dates 2026 confirmées")
