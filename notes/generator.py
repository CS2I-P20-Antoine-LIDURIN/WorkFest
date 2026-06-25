import os

from config.settings import OUTPUT_DIR

from notes.writers import (
write_festival_note,
write_month_notes,
write_no_date_note,
write_index,
)

def generate_notes(festivals_data):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True,
    )

    notes_dir = os.path.join(
        OUTPUT_DIR,
        "festivals",
    )

    os.makedirs(
        notes_dir,
        exist_ok=True,
    )

    by_month = {}
    no_date = []

    for festival in festivals_data:

        write_festival_note(
            notes_dir,
            festival,
        )

        if festival["month"]:

            by_month.setdefault(
                festival["month"],
                []
            ).append(
                festival
            )

        else:

            no_date.append(
                festival
            )

    write_month_notes(
        by_month
    )

    write_no_date_note(
        no_date
    )

    write_index(
        festivals_data,
        by_month,
        no_date,
)