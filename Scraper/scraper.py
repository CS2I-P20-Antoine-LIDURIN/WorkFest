import re

from bs4 import BeautifulSoup

from config.settings import HEADERS

from scraper.dates import (
    extract_dates,
)

from scraper.helpers import (
    get_page_title,
    get_description,
    clean_page,
    get_full_text,
    extract_artists,
)


def scrape_festival(name, url, genre, ville):

    result = {
        "name": name,
        "url": url,
        "genre": genre,
        "ville": ville,
        "statut": "ok",
    }

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "lxml",
        )

    except Exception as error:

        result["statut"] = str(error)


    soup = BeautifulSoup(
        response.text,
        "lxml",
    )

    result["titre_page"] = (
        get_page_title(
            soup
        )
    )

    result["description"] = (
        get_description(
            soup
        )
    )

    soup = clean_page(
        soup
    )

    full_text = get_full_text(
        soup
    )

    (
        result["dates_2026"],
        result["month"],
    ) = extract_dates(
        full_text
    )

    result["artistes"] = (
        extract_artists(
            soup
        )
    )
    return result