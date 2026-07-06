from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain.tools import tool

import os
from dotenv import load_dotenv

load_dotenv()

# -------------------- // --------------------
# 1. Load pdf
file_paths = ["./files/employee_handbook_v2.pdf", "./files/project_lunar_base_omega.pdf"]
documents = []

for path in file_paths:
    loader = PyPDFLoader(path)
    documents.extend(loader.load()) # different from append, unpacks and adds items individually

print(f"Loaded documents: {len(documents)}")

# -------------------- // --------------------
# 2. Chunkerization

# 2.1 create splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

# 2.2 create chunks
docs = text_splitter.split_documents(documents)
print (f"Created chunks: {len(docs)}")

# -------------------- // --------------------
# 3. Create DB

persist_directory = "./chroma_db"
hr_collection = "human_resources_docs"
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

vector_store = Chroma(persist_directory=persist_directory, 
                      embedding_function=embeddings,
                      collection_name=hr_collection) #creates db pointing to specific collections

if vector_store._collection.count() > 0: # checks if collection used has records
    print("Data already loaded! Ready to go.")
else:
    print("Collection is empty. Generating embeddings...")
    vector_store.add_documents(docs)

# -------------------- // --------------------
# 4. Retriever comes in as a TOOL.

@tool(response_format="content_and_artifact") # tool returns serialized text and original docs, to be saved on agent state
def search_on_doc(query: str) -> tuple:
    """
    Looks up information on the loaded document.
    Use this anytime the user makes questions related to the Human Resources manuals used for answering.
        
    Args:
        query: question asked by user
    
    Returns:
        dict: a dictionary with the `content` key with serialized information
    """
    
    retrieved_docs = vector_store.similarity_search(query=query, k=2,)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\n Content: {doc.page_content}"
        for doc in retrieved_docs
        )
    
    return serialized, retrieved_docs
    

# -------------------- // --------------------

model = init_chat_model("openai:gpt-5.4-mini", temperature=0)

agent = create_agent(
    model=model,
    system_prompt="You`re an HR assistant that answer questions about Nexus Corp,"
                "Use the tool provided to look up information from the company documents."
                "If you can't find the answer to something, politely say you do not know.",
    tools=[search_on_doc]
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# langraph dev
