import os

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")

DELAY = 1.5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

MONTHS_FR = {
    1:"Janvier",
    2:"Février",
    3:"Mars",
    4:"Avril",
    5:"Mai",
    6:"Juin",
    7:"Juillet",
    8:"Août",
    9:"Septembre",
    10:"Octobre",
    11:"Novembre",
    12:"Décembre",
}