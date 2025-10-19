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

def get_weather_data(country: str) -> str:
    """
    Get weather data directly from the country's weather file.
    
    Args:
        country: Name of the country
    
    Returns:
        Weather data as string or None if file not found
    """
    data_dir = Path(__file__).parent.parent / "data" / "weather"
    file_path = data_dir / f"{country.lower()}_weather.txt"
    
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"No weather data found for {country}")
            return None
    except Exception as e:
        print(f"Error reading weather data for {country}: {e}")
        return None

class RAGAssistant:
    def __init__(self):
        """Initialize the RAG assistant."""
        self.llm = self._initialize_llm()
        if not self.llm:
            raise ValueError(
                "No valid API key found. Please set one of: "
                "OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

        # Weather-specific prompt template
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a weather information assistant. Analyze the weather data provided and give recommendations.

        Weather Data for {country}:
        {weather_data}

        Please provide a detailed analysis in the following format:

        # Weather Report for {country}

        ## Current Weather Conditions
        [Provide exact temperature, humidity, and weather conditions from the data]

        ## Weather-based Recommendations
        [Suggest appropriate activities and precautions based on current conditions]

        ## Travel Advisory
        [Provide specific advice for travelers based on the current weather]

        Note: Base all recommendations strictly on the provided weather data.
        Do not make assumptions or add information not in the data file.
        """)
        
        # Create the chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()

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

    def invoke(self, country: str) -> str:
        """
        Generate weather advisory for a specific country.

        Args:
            country: Name of the country

        Returns:
            Weather analysis and recommendations
        """
        try:
            weather_data = get_weather_data(country)
            
            if not weather_data:
                return f"No weather data available for {country}"
            
            # Generate analysis using the chain
            result = self.chain.invoke({
                "country": country,
                "weather_data": weather_data
            })
            
            return result

        except Exception as e:
            print(f"Error generating weather advisory: {str(e)}")
            return "I encountered an error while processing your request."

def main():
    """Main function to demonstrate the weather advisory assistant."""
    try:
        print("Initializing Weather Advisory Assistant...")
        assistant = RAGAssistant()

        while True:
            country = input("\nEnter a country name or 'quit' to exit: ").strip()
            
            if country.lower() == 'quit':
                break
            
            print("\nGenerating weather advisory...")
            result = assistant.invoke(country)
            print("\n" + result)

    except Exception as e:
        print(f"Error running Weather Advisory Assistant: {e}")
        print("\nMake sure you have:")
        print("1. Weather data files in data/weather directory (e.g., india_weather.txt)")
        print("2. At least one API key set in your .env file:")
        print("   - OPENAI_API_KEY (OpenAI GPT models)")
        print("   - GROQ_API_KEY (Groq Llama models)")
        print("   - GOOGLE_API_KEY (Google Gemini models)")

if __name__ == "__main__":
    main()
