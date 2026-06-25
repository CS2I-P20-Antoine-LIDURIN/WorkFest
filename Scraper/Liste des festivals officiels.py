import requests
import os
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup

#Configuration

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
DELAY      = 1.5   # secondes entre chaque requête (respecter les serveurs)
HEADERS    = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

MONTHS_FR = {
    1:  "Janvier",   2: "Février",   3: "Mars",      4: "Avril",
    5:  "Mai",       6: "Juin",      7: "Juillet",   8: "Août",
    9:  "Septembre", 10: "Octobre",  11: "Novembre", 12: "Décembre",
}


#Liste des festivals officiels


FESTIVALS = [
    # ── Rock / Metal ──
    ("Hellfest",                    "https://www.hellfest.fr",                    "Metal",           "Clisson"),
    ("Rock en Seine",               "https://www.rockenseine.com",                "Rock",            "Saint-Cloud"),
    ("Download Festival Paris",     "https://downloadfestival.fr",               "Metal/Rock",      "Paris"),
    ("Eurockéennes de Belfort",     "https://www.eurockeennes.fr",               "Rock",            "Belfort"),
    ("Cabaret Vert",                "https://www.cabaretvert.com",               "Rock/Alternatif", "Charleville-Mézières"),
    ("Main Square Festival",        "https://www.mainsquarefestival.fr",         "Rock/Pop",        "Arras"),
    ("Garorock",                    "https://www.garorock.com",                  "Rock/Hip-Hop",    "Marmande"),

    # ── Pop / Généraliste ──
    ("Les Vieilles Charrues",       "https://www.vieillescharrues.asso.fr",      "Pop/Rock",        "Carhaix"),
    ("Solidays",                    "https://www.solidays.org",                  "Électro/Pop",     "Paris"),
    ("Lollapalooza Paris",          "https://www.lollapaloozafr.com",            "Pop/Rock/Électro","Paris"),
    ("We Love Green",               "https://www.welovegreenmusic.com",          "Pop/Électro",     "Paris"),
    ("Printemps de Bourges",        "https://www.printemps-bourges.com",         "Pop/Rock",        "Bourges"),
    ("Musilac",                     "https://www.musilac.com",                   "Pop/Rock",        "Aix-les-Bains"),
    ("Les Déferlantes",             "https://lesdeferlantes.com",                "Pop",             "Argelès-sur-Mer"),

    # ── Électro / Dance ──
    ("Nuits Sonores",               "https://www.nuits-sonores.com",             "Électronique",    "Lyon"),
    ("Peacock Society",             "https://www.peacocksociety.fr",             "Électronique",    "Paris"),
    ("Delta Festival",              "https://deltafestival.com",                 "Électronique",    "Marseille"),
    ("Marsatac",                    "https://www.marsatac.com",                  "Électronique",    "Marseille"),

    # ── Jazz / Blues ──
    ("Jazz in Marciac",             "https://www.jazzinmarciac.com",             "Jazz",            "Marciac"),
    ("Jazz à Juan",                 "https://jazzajuan.com",                     "Jazz",            "Juan-les-Pins"),
    ("Les Rendez-vous de l'Erdre",  "https://www.rendezvousdelerdre.com",        "Jazz/Classique",  "Nantes"),

    # ── Francophone / Variété ──
    ("Francofolies de La Rochelle", "https://www.francofolies.fr",               "Chanson/Pop FR",  "La Rochelle"),
    ("Les Trans Musicales",         "https://www.lestrans.com",                  "Émergence",       "Rennes"),

    # ── Hip-Hop / Urban ──
    ("Booska Summer Festival",      "https://www.booskasummerland.com",          "Hip-Hop",         "Ile-de-France"),

    # ── Celtique / Folk / Monde ──
    ("Festival Interceltique de Lorient", "https://festival-interceltique.bzh",  "Celtique",        "Lorient"),
    ("Terres du Son",               "https://www.terresduson.com",               "Monde/Rock",      "Indre-et-Loire"),

    # ── Classique ──
    ("Festival de Radio France",    "https://www.festival-radio-france.fr",      "Classique/Jazz",  "Montpellier"),
    ("Chorégies d'Orange",          "https://www.choregies.fr",                  "Opéra",           "Orange"),

    # ── Reggae ──
    ("Reggae Sun Ska",              "https://www.reggaesunskaofficial.com",      "Reggae",          "Bordeaux"),

    # ── Multi-genre ──
    ("Art Rock",                    "https://www.artrock.fr",                    "Éclectique",      "Saint-Brieuc"),
    ("Festival de Cornouaille",     "https://www.festival-cornouaille.bzh",      "Breton/Monde",    "Quimper"),
    ("Beauregard Festival",         "https://www.beauregardfestival.com",        "Rock/Pop",        "Hérouville-Saint-Clair"),
    ("Panoramas",                   "https://www.panoramas.fr",                  "Électro/Rock",    "Morlaix"),
    ("Fête de l'Humanité",          "https://www.fetedelhumanite.fr",            "Éclectique",      "Plaine Saint-Denis"),
]


