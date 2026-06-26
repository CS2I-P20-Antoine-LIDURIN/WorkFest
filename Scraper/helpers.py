import re


def get_page_title(soup):
    title = soup.find("title")
    if title:
        return title.get_text(strip=True)
    return ""


def get_description(soup):
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        prop = meta.get("property", "").lower()
        if name in ("description", "og:description") or prop == "og:description":
            content = meta.get("content", "").strip()
            if content:
                return content

    for container_tag in ("main", "article"):
        container = soup.find(container_tag)
        if container:
            for p in container.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) > 80:
                    return text

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 80:
            return text

    return ""


def clean_page(soup):
    for tag in soup(["script", "style", "footer", "aside"]):
        tag.decompose()
    return soup


def get_full_text(soup):
    for container_tag in ("main", "article"):
        container = soup.find(container_tag)
        if container:
            text = container.get_text(separator="\n")
            text = re.sub(r"\n{3,}", "\n\n", text)
            return text.strip()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_artists(soup):
    artists = []

    pattern = re.compile(
        r"artist|lineup|artiste|performer|"
        r"programmation|programme|acts|headliner|"
        r"affiche|casting",
        re.I,
    )

    sections = soup.find_all(attrs={"class": pattern})

    if len(sections) < 2:
        for container_tag in ("main", "article", "section"):
            container = soup.find(container_tag)
            if container:
                sections.append(container)
                break

    seen = set()
    for section in sections[:5]:
        for item in section.find_all(["li", "span", "div", "p", "h3", "h4"])[:30]:
            text = item.get_text(strip=True)
            if 2 < len(text) < 60 and text not in seen:
                seen.add(text)
                artists.append(text)
        if len(artists) >= 20:
            break

    return artists[:20]