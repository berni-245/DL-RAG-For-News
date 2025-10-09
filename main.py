import streamlit as st
from src.scraping import InfobaeScraper

def main():
    st.title("📰 Scraping Infobae")

    if "news" not in st.session_state:
        st.session_state.news = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # --- Botón para scrapear ---
    if st.button("Scrapear noticias"):
        scraper = InfobaeScraper()
        try:
            st.session_state.news = scraper.scrape_rss()
            st.session_state.current_index = 0
            st.success("Noticias obtenidas correctamente ✅")
        except Exception as e:
            st.error(f"Error al scrapear la página: {e}")

    # --- Botón para limpiar resultados ---
    if st.button("Limpiar"):
        st.session_state.news.clear()
        st.session_state.current_index = 0
        st.info("Noticias borradas 🧹")

    def next_news():
        if st.session_state.current_index < len(st.session_state.news) - 1:
            st.session_state.current_index += 1

    def prev_news():
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1

    # --- Mostrar navegación y contenido ---
    if st.session_state.news:
        total = len(st.session_state.news)
        index = st.session_state.current_index

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.button("⬅️ Anterior", on_click=prev_news)

        with col3:
            st.button("Siguiente ➡️", on_click=next_news)

        st.markdown(f"### Mostrando noticia {index + 1} de {total}")
        st.markdown(st.session_state.news[index])


if __name__ == "__main__":
    main()
