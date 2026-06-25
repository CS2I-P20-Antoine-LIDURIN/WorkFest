import os
import re

from datetime import datetime

from config.settings import (
OUTPUT_DIR,
MONTHS_FR,
)

def safe_filename(name):

    return re.sub(
        r'[\\/*?:"<>|]',
        "-",
        name,
)

def write_festival_note(
    notes_dir,
    festival,
    ):

    filename = (
        safe_filename(
            festival["name"]
        )
        + ".md"
    )

    path = os.path.join(
        notes_dir,
        filename,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(f"""# {festival["name"]}
    ```

    ## Informations

    * Ville : {festival["ville"]}
    * Genre : {festival["genre"]}
    * Site : {festival["url"]}
      """)

        if festival["dates_2026"]:

            file.write(
                "\n- Dates : "
                + " | ".join(
                    festival["dates_2026"]
                )
                + "\n"
            )

        if festival["description"]:

            file.write(f"""
      ```

    ## Description

    {festival["description"]}
    """)

        if festival["artistes"]:

            file.write(
                "\n## Artistes\n\n"
            )

            for artist in festival["artistes"]:

                file.write(
                    f"- {artist}\n"
                )

def write_month_notes(
    by_month,
    ):

    for month_num, events in by_month.items():

        path = os.path.join(
            OUTPUT_DIR,
            f"{month_num:02d}-{MONTHS_FR[month_num]}.md",
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                f"# {MONTHS_FR[month_num]} 2026\n\n"
            )

            for event in events:

                file.write(
                    f"- {event['name']}\n"
                )

def write_no_date_note(
    festivals,
    ):

    if not festivals:
        return

    path = os.path.join(
        OUTPUT_DIR,
        "Sans-date.md",
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "# Festivals sans date\n\n"
        )

        for festival in festivals:

            file.write(
                f"- {festival['name']}\n"
            )

def write_index(
    festivals_data,
    by_month,
    no_date,
    ):

    path = os.path.join(
        OUTPUT_DIR,
        "INDEX.md",
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(f"""# Festivals France 2026
    ```

    Généré le {datetime.now().strftime("%d/%m/%Y %H:%M")}

    Nombre de festivals : {len(festivals_data)}

    ## Mois disponibles

    """)

        for month in sorted(
            by_month.keys()
        ):

            file.write(
                f"- {MONTHS_FR[month]}\n"
            )

        if no_date:

            file.write(
                "- Sans date\n"
            )
