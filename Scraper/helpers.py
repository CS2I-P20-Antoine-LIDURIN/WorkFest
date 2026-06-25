import re

def get_page_title(soup):
    title = soup.find("title")
    if title:
        return title.get_text(strip=True)
    return ""


def get_description(soup):
    for meta in soup.find_all("meta"):
        if (
            meta.get("name", "").lower()
            in ["description", "og:description"]
            or
            meta.get("property", "").lower()
            == "og:description"
        ):
            content = meta.get(
                "content",
                ""
            ).strip()
            if content:
                return content
    return ""


def clean_page(soup):
    for tag in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
        ]
    ):
        tag.decompose()
    return soup


def get_full_text(soup):
    text = soup.get_text(
        separator="\n"
    )
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )
    return text.strip()


def extract_artists(soup):
    artists = []
    sections = soup.find_all(
        attrs={
            "class": re.compile(
                r"artist|lineup|artiste|performer",
                re.I,
            )
        }
    )

    for section in sections[:3]:
        for item in section.find_all(
            [
                "li",
                "span",
                "div",
                "p",
                "h3",
                "h4",
            ]
        )[:20]:

            text = item.get_text(
                strip=True
            )
            if (
                2 < len(text) < 60
                and text not in artists
            ):
                artists.append(text)

    return artists[:20]