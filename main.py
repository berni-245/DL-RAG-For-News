import streamlit as st
from src.scraping import scrape_infobae_page

def main():
    st.title("Scraping Infobae")
    with st.form("scraping_form"):
        url = st.text_input("Pegá el link de la nota de Infobae:")

        if st.form_submit_button("Scrapear artículo"):
            if url.strip():
                try:
                    result = scrape_infobae_page(url.strip())
                    st.success("Artículo obtenido correctamente ✅")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error al scrapear la página: {e}")
            else:
                st.warning("Por favor ingresá un link válido.")

if __name__ == "__main__":
    main()
