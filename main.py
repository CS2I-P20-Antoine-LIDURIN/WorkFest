import time

from config.settings import (
    DELAY,
)

from config.festivals import (
    FESTIVALS,
)

from scraper.scraper import (
    scrape_festival,
)

from notes.generator import (
    generate_notes,
)


def main():

    print(
        "GW05 - Scraper festivals France 2026"
    )

    print(
        f"{len(FESTIVALS)} festivals"
    )

    results = []

    for index, festival in enumerate(
        FESTIVALS,
        start=1,
    ):

        print(
            f"[{index}/{len(FESTIVALS)}] {festival[0]}"
        )

        results.append(
            scrape_festival(
                *festival
            )
        )

        time.sleep(
            DELAY
        )

    print(
        "Génération des notes Obsidian..."
    )

    generate_notes(results)

    print(
        "Terminé"
    )


if __name__ == "__main__":
    main()