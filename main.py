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
        "Terminé"
    )


if __name__ == "__main__":
    main()