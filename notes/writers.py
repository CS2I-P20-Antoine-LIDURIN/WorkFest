import os
import re

from datetime import datetime

from config.settings import (
    OUTPUT_DIR,
    MONTHS_FR,
)


def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "-", name)


def write_festival_note(notes_dir, festival):

    filename = safe_filename(festival["name"]) + ".md"
    path = os.path.join(notes_dir, filename)

    with open(path, "w", encoding="utf-8") as f:

        f.write(f"# {festival['name']}\n\n")

        if festival.get("statut") and festival["statut"] != "ok":
            f.write(f"> ⚠️ Site inaccessible : {festival['statut']}\n\n")

        f.write("## Informations\n\n")
        f.write("| Champ | Valeur |\n")
        f.write("|-------|--------|\n")
        f.write(f"| 📍 Ville  | {festival.get('ville', '')} |\n")
        f.write(f"| 🎸 Genre  | {festival.get('genre', '')} |\n")

        if festival.get("dates_2026"):
            f.write(f"| 📅 Dates  | {' · '.join(festival['dates_2026'])} |\n")

        f.write(f"| 🌐 Site   | [{festival.get('url', '')}]({festival.get('url', '')}) |\n")
        f.write("\n")

        if festival.get("description"):
            f.write("## Description\n\n")
            f.write(f"{festival['description']}\n\n")

        if festival.get("artistes"):
            f.write("## Artistes\n\n")
            for artiste in festival["artistes"]:
                f.write(f"- {artiste}\n")
            f.write("\n")

        f.write("---\n\n[[INDEX|← Retour à l'index]]\n")


def write_month_notes(by_month):

    for month_num, events in sorted(by_month.items()):

        month_name = MONTHS_FR[month_num]
        path = os.path.join(
            OUTPUT_DIR,
            f"2026-{month_num:02d}-{month_name}.md",
        )

        with open(path, "w", encoding="utf-8") as f:

            f.write(f"# 🎵 Festivals — {month_name} 2026\n\n")
            f.write(f"> {len(events)} festival(s) · [[INDEX|← Index]]\n\n---\n\n")

            for evt in sorted(events, key=lambda x: x["name"]):
                safe = safe_filename(evt["name"])
                f.write(f"## [[festivals/{safe}|{evt['name']}]]\n\n")
                f.write(f"- 📍 **Ville** : {evt.get('ville', '')}\n")
                f.write(f"- 🎸 **Genre** : {evt.get('genre', '')}\n")
                if evt.get("dates_2026"):
                    f.write(
                        f"- 📅 **Dates** : {' · '.join(evt['dates_2026'][:2])}\n"
                    )
                if evt.get("description"):
                    desc = evt["description"][:200]
                    f.write(f"\n> {desc}\n")
                f.write("\n---\n\n")


def write_no_date_note(festivals):

    if not festivals:
        return

    path = os.path.join(OUTPUT_DIR, "2026-00-Sans-date.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# 🎵 Festivals — Date non trouvée sur le site\n\n")
        f.write(
            f"> {len(festivals)} festival(s) · [[INDEX|← Index]]\n\n---\n\n"
        )
        for festival in sorted(festivals, key=lambda x: x["name"]):
            safe = safe_filename(festival["name"])
            f.write(
                f"- [[festivals/{safe}|{festival['name']}]]"
                f" — {festival.get('ville', '')} · {festival.get('genre', '')}\n"
            )


def write_index(festivals_data, by_month, no_date):

    path = os.path.join(OUTPUT_DIR, "INDEX.md")
    total = len(festivals_data)
    confirmed = sum(1 for f in festivals_data if f.get("dates_2026"))

    with open(path, "w", encoding="utf-8") as f:

        f.write("# 🎵 Festivals de musique en France — 2026\n\n")
        f.write("> Source : sites officiels de chaque festival  \n")
        f.write(
            f"> Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}  \n"
        )
        f.write(
            f"> **{total} festivals** · **{confirmed} avec dates 2026 confirmées** ✅\n\n"
        )
        f.write("## 📅 Par mois\n\n")

        for month_num in sorted(by_month.keys()):
            name = MONTHS_FR[month_num]
            events = by_month[month_num]
            count = len(events)
            confirmed_month = sum(1 for e in events if e.get("dates_2026"))
            f.write(
                f"- [[2026-{month_num:02d}-{name}]]"
                f" — {count} festival(s) *(dont {confirmed_month} confirmés ✅)*\n"
            )

        if no_date:
            f.write(
                f"- [[2026-00-Sans-date]] — {len(no_date)} sans date\n"
            )

        f.write("\n## 🗂️ Tous les festivals\n\n")

        for festival in sorted(festivals_data, key=lambda x: x["name"]):
            safe = safe_filename(festival["name"])
            tick = " ✅" if festival.get("dates_2026") else ""
            f.write(
                f"- [[festivals/{safe}|{festival['name']}]]{tick}"
                f" — {festival.get('ville', '')}\n"
            )