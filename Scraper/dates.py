import re

MONTH_NAMES_PATTERN = (
    r"janvier|f[eé]vrier|mars|avril|mai|juin|juillet|"
    r"ao[uû]t|septembre|octobre|novembre|d[eé]cembre"
)

DATE_2026_RE = re.compile(
    rf"(?:{MONTH_NAMES_PATTERN}\s+2026|\d{{2}}[/-]\d{{2}}[/-]2026|2026[/-]\d{{2}}[/-]\d{{2}})",
    re.IGNORECASE
)

MONTH_MAP = {
    "janvier": 1,
    "fevrier": 2,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "decembre": 12,
    "décembre": 12,
}


def extract_dates(text):
    dates = list(
        dict.fromkeys(
            DATE_2026_RE.findall(text)
        )
    )
    dates = dates[:6]
    month = None

    for date in dates:
        lower = date.lower()
        for month_name, month_number in MONTH_MAP.items():
            if month_name in lower:
                month = month_number
                return dates, month
        match = re.search(
            r"2026[-/](\d{2})",
            date
        )
        
        if match:
            month = int(match.group(1))
            return dates, month
        
    return dates, month