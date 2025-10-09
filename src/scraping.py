import requests
from bs4 import BeautifulSoup

class InfobaeScraper:
    def __init__(self):
        self.rss_url = "https://www.infobae.com/arc/outboundfeeds/rss/"
    def scrape_rss(self):
        page = requests.get(self.rss_url)
        soup = BeautifulSoup(page.content, 'xml')

        item = soup.find('item')
        assert item is not None, "No se encontró ningún <item> en el feed RSS."

        metadata_md = self._scrape_metadata(item)

        content_tag = item.find('content:encoded')
        assert content_tag is not None, "The item doesn't have a <content:encoded> tag."
        inner_html_parsed = self._scrape_content(content_tag.text)

        result = metadata_md + "\n" + inner_html_parsed
        return result

    def _scrape_metadata(self, item):
        title = item.find('title').get_text(strip=True)
        link = item.find('link').get_text(strip=True)
        pub_date = item.find('pubDate').get_text(strip=True)
        creator = item.find('dc:creator').get_text(strip=True)
        description = item.find('description').get_text(strip=True)

        metadata_md = f"""# {title}

    **Descripción:** {description}
    **Link:** [{link}]({link})  
    **Fecha de publicación:** {pub_date}  

    ---
        """
        return metadata_md

    def _scrape_content(self, inner_html: str) -> str:
        """Convierte el HTML de <content:encoded> en Markdown limpio."""
        soup = BeautifulSoup(inner_html, 'html.parser')

        content = []
        label_to_md = {
            "H1": "#",
            "H2": "##",
            "H3": "###"
        }
        for tag in soup.find_all(True):
            if tag.name in ["h1", "h2", "h3"]:
                text = tag.get_text(strip=True)
                if text:
                    content.append(f"{label_to_md[tag.name.upper()]} {text}")
            elif tag.name == "p":
                text = tag.get_text().strip()
                if text:
                    content.append(text)

        result = "\n\n".join(content)
        return result