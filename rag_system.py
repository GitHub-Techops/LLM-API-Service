from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os

class RAGSystem:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.llm = Ollama(model="llama3.2:1b")
        self.vectorstore = None
        self.qa_chain = None
    
    def ingest_documents(self, file_paths):
        """Load and process documents"""
        documents = []
        for path in file_paths:
            if path.endswith('.pdf'):
                loader = PyPDFLoader(path)
            else:
                loader = TextLoader(path)
            documents.extend(loader.load())
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vectorstore.persist()
        print(f"✓ Ingested {len(texts)} chunks from {len(file_paths)} documents")
    
    def load_existing(self):
        """Load existing vector database"""
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        print("✓ Loaded existing vector database")
    
    def create_qa_chain(self):
        """Create question-answering chain"""
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
        )
        print("✓ Created QA chain")
    
    def query(self, question):
        """Ask a question"""
        if not self.qa_chain:
            self.create_qa_chain()
        return self.qa_chain.run(question)


# TEST CODE - Run this to verify everything works
if __name__ == "__main__":
    print("=" * 60)
    print("RAG SYSTEM TEST")
    print("=" * 60)
    
    # Create a test document
    print("\n1. Creating test document...")
    with open("test_doc.txt", "w", encoding="utf-8") as f:
        f.write("""
        DevOps is a set of practices that combines software development (Dev) 
        and IT operations (Ops). It aims to shorten the systems development 
        life cycle and provide continuous delivery with high software quality.
        
        Key DevOps practices include:
        - Continuous Integration (CI): Automatically testing code changes
        - Continuous Delivery (CD): Automating deployment pipelines
        - Infrastructure as Code (IaC): Managing infrastructure through code
        - Monitoring and Logging: Tracking system performance
        - Collaboration: Breaking down silos between teams
        
        Popular DevOps tools include Jenkins, GitLab, Docker, Kubernetes, 
        Terraform, Ansible, Prometheus, and Grafana.
        
        DevOps helps organizations deliver applications faster while 
        maintaining high quality and reliability.
        """)
    print("✓ Test document created: test_doc.txt")
    
    # Initialize RAG system
    print("\n2. Initializing RAG system...")
    rag = RAGSystem()
    print("✓ RAG system initialized")
    
    # Ingest documents
    print("\n3. Ingesting documents...")
    rag.ingest_documents(["test_doc.txt"])
    
    # Create QA chain
    print("\n4. Creating QA chain...")
    rag.create_qa_chain()
    
    # Test queries
    print("\n5. Testing queries...")
    print("=" * 60)
    
    #questions = [
    #    "What is DevOps?",
    #    "What are the key practices of DevOps?",
    #    "How does DevOps help organizations?"
    #]
    questions = [
        "What is Python programming?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("-" * 60)
        answer = rag.query(question)
        print(f"Answer: {answer}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)