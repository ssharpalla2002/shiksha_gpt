from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

DATA_PATH = 'data/'
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader) # We load the pdfs present in the directory

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50) # We initialize the text_splitter function
    texts = text_splitter.split_documents(documents)# We split the loaded documents into chunks 

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'}) # we initialize our sentence transformers model along with the device tobe used 

    db = FAISS.from_documents(texts, embeddings,allow_dangerous_deserialization=True)# perform the sentence transformation leading to formation of vector embeddings
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()

