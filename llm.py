from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.scraping import InfobaeScraper

infobae_scraper = InfobaeScraper()

results = infobae_scraper.scrape_rss()

# TODO Add logging maybe
def get_docs(markdowns: list[str]):
    # TODO Evaluate how to add metadata here
    return [Document(page_content=md) for md in markdowns]

def split_docs(docs, chunk_size=2000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True, # This is to add a starting index to the chunks, useful to reconstruct the original document from the chunks.
        separators=["\n---", "\n## ", "\n### ", "\n", " "]
    )
    chunks = text_splitter.split_documents(docs)

    return chunks






