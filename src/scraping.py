import requests
from bs4 import BeautifulSoup

def scrape_infobae_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    content = []
    label_to_md = {
        "H1": "#",
        "H2": "##",
        "H3": "###"
    }
    # Recorremos todos los elementos en orden
    for tag in soup.find_all(True):
        assert tag is not None
        # Cortar cuando aparezca el div con clase "second-saved-buttons"
        if tag.name == "div" and "second-saved-buttons" in (tag.get("class") or []): 
            break  

        if tag.name in ["h1", "h2", "h3"]:
            text = tag.get_text(strip=True)
            if text:
                content.append(f"{label_to_md[tag.name.upper()]} {text}")

        elif tag.name == "p" and "paragraph" in (tag.get("class") or []):
            text = tag.get_text().strip()
            if text:
                content.append(text)

    result = "\n\n".join(content)
    with open ("last_article.md", "w") as f:
        f.write(result)
    return result