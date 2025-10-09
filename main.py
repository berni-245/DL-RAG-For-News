import streamlit as st
from src.scraping import InfobaeScraper

def main():
    st.title("Scraping Infobae")
    with st.form("scraping_form"):
        if st.form_submit_button("Scrapear artículo"):
            scraper = InfobaeScraper()
            try:
                result = scraper.scrape_rss()
                st.success("Artículo obtenido correctamente ✅")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error al scrapear la página: {e}")

if __name__ == "__main__":
    main()
