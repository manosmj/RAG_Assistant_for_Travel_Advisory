import os
from typing import List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vectordb import VectorDB
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path

# Load environment variables
load_dotenv()

def load_documents() -> List[str]:
    """
    Load documents for demonstration.

    Returns:
        List of sample documents
    """
    results = []
    # Define data directory relative to current file
    data_dir = Path(__file__).parent.parent / "data" / "weather"
    
    if not data_dir.exists():
        print(f"Data directory does not exist: {data_dir}")
        return results

    print(f"Loading documents from: {data_dir}")

    # Process only .txt files
    for file_path in data_dir.glob("*.txt"):
        try:
            print(f"Processing: {file_path.name}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            results.append({
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    "type": "txt",
                    "path": str(file_path)
                }
            })
            print(f"Successfully loaded: {file_path.name}")
        except Exception as e:
            print(f"Error loading {file_path.name}: {str(e)}")
            continue

    print(f"Loaded {len(results)} text documents")        
    return results


class RAGAssistant:
    """
    A simple RAG-based AI assistant using ChromaDB and multiple LLM providers.
    Supports OpenAI, Groq, and Google Gemini APIs.
    """

    def __init__(self):
        """Initialize the RAG assistant."""
        # Initialize LLM - check for available API keys in order of preference
        self.llm = self._initialize_llm()
        if not self.llm:
            raise ValueError(
                "No valid API key found. Please set one of: "
                "OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

        # Initialize vector database
        self.vector_db = VectorDB()

        # RAG prompt template
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant. Answer the question based on the provided context.
        If you cannot find the answer in the context, say "I don't have enough information to answer this question."
        Do not make up or infer information that is not in the context.

        Context:
        {context}

        Question:
        {question}

        Answer:""")
        # Create the chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()

        print("RAG Assistant initialized successfully")

    def _initialize_llm(self):
        """
        Initialize the LLM by checking for available API keys.
        Tries OpenAI, Groq, and Google Gemini in that order.
        """
        # Check for OpenAI API key
        if os.getenv("OPENAI_API_KEY"):
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            print(f"Using OpenAI model: {model_name}")
            return ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GROQ_API_KEY"):
            model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            print(f"Using Groq model: {model_name}")
            return ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GOOGLE_API_KEY"):
            model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
            print(f"Using Google Gemini model: {model_name}")
            return ChatGoogleGenerativeAI(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                model=model_name,
                temperature=0.0,
            )

        else:
            raise ValueError(
                "No valid API key found. Please set one of: OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

    def add_documents(self, documents: List) -> None:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of documents
        """
        self.vector_db.add_documents(documents)

    def invoke(self, input: str, n_results: int = 3) -> str:
        """
        Query the RAG assistant.

        Args:
            input: User's input
            n_results: Number of relevant chunks to retrieve

        Returns:
            Dictionary containing the answer and retrieved context
        """
        try:
            # Search for relevant context chunks
            search_results = self.vector_db.search(input, n_results=n_results)
        
            if not search_results["documents"]:
                return "I don't have any relevant information to answer this question."
            
            # Combine retrieved chunks into a single context string
            context = "\n\n".join(search_results["documents"])
        
            # Generate answer using the chain
            llm_answer = self.chain.invoke({
                "context": context,
                "question": input
            })
            
            return llm_answer

        except Exception as e:
            print(f"Error in RAG pipeline: {str(e)}")
            return "I encountered an error while processing your question."

def main():
    """Main function to demonstrate the RAG assistant."""
    try:
        # Initialize the RAG assistant
        print("Initializing RAG Assistant...")
        assistant = RAGAssistant()

        # Load sample documents
        print("\nLoading documents...")
        sample_docs = load_documents()
        print(f"Loaded {len(sample_docs)} sample documents")

        assistant.add_documents(sample_docs)

        done = False

        while not done:
            question = input("Enter a question or 'quit' to exit: ")
            if question.lower() == "quit":
                done = True
            else:
                result = assistant.invoke(question)
                print(result)

    except Exception as e:
        print(f"Error running RAG assistant: {e}")
        print("Make sure you have set up your .env file with at least one API key:")
        print("- OPENAI_API_KEY (OpenAI GPT models)")
        print("- GROQ_API_KEY (Groq Llama models)")
        print("- GOOGLE_API_KEY (Google Gemini models)")


if __name__ == "__main__":
    main()
