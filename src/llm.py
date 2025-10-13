import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from scraping import InfobaeScraper
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI


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

def get_data_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}     
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    return db

def get_chain(db):
    llm = ChatOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=os.environ["GITHUB_TOKEN"],
        model_name="gpt-4o-mini",
        max_tokens=256
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_type="similarity", search_kwargs={"k": 2}),
        verbose=False
    )
    return chain

infobae_scraper = InfobaeScraper()

results = infobae_scraper.scrape_rss()

load_dotenv()

docs = get_docs(results)
chunks = split_docs(docs)
db = get_data_store(chunks)
chain = get_chain(db)

print("Chatbot: Hola! ¿Qué noticia deseas saber?")

user_input = ""

while user_input != "bye":
    user_input = input("You: ")
    response = chain.run(user_input + "Solo responde en español y meté enter cada 10 palabras. Solo responde información con el contexto proporcinado. En caso de no tener información responde 'Lo siento no tengo esa información'") # Get chatbot response to user prompt
    print(f"Chatbot: {response}")





