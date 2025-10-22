
# 🤖 RAG-Based Travel Assistant

This application is a user-friendly tool for obtaining real-time weather data and relevant travel advice for any country in the world. By simply entering a country name, users can instantly access key weather metrics and receive curated tips to help them plan their trip effectively. This app leverages Open Weather API to provide accurate, up-to-date information, making it a convenient resource for travelers, students, or anyone interested in global weather patterns.

Features:

- RAG (Retrieval-Augmented Generation) travel assistant core:
  - Retrieval + generation pipeline that searches a vector DB for relevant context and uses an LLM to generate answers.
  - Combines retrieved chunks into context and runs a prompt → LLM → output parser chain.

- Document ingestion and vectorization:
  - Functions to get current weather data of each country using OpenWeather API.
  - Functions to load and add weather data to a vector store.
  - Vector DB abstraction (vectordb module) used for indexing and searching.

- Retrieval configuration and usage:
  - add_documents(documents: List) to populate the knowledge base.
  - invoke(input, n_results=3) runs a search, assembles context, and queries the LLM chain.
  - Handles missing results and basic error handling.

- Weather-specific travel advisory app:
  - weather_app.py provides a weather-focused prompt template and a dedicated RAGAssistant for weather analysis.
  - get_weather_data(country) reads weather files (expects data/weather directory files like india_weather.txt).
  - invoke(country) returns an LLM-generated weather analysis using the provided weather data and a structured prompt.

- Local travel-advisory logic:
  - travel_advisory.py contains generate_travel_advisory(country) that reads weather data and composes a formatted advisory (clothing, activities, precautions) from parsed temperature, humidity, and condition values.
  - Provides a non-LLM, rule-based advisory generation path.

- Prompting and output parsing:
  - Uses ChatPromptTemplate for structured prompts (general and weather-specific).
  - Uses StrOutputParser to produce string outputs from the chain pipeline.

- Environment and setup guidance:
  - Uses dotenv for environment variables and provides instructions to set API keys (OPENAI_API_KEY, GROQ_API_KEY, GOOGLE_API_KEY).
  - README lists required pieces (weather data files, .env keys) and startup notes.

- Extensibility and configuration:
  - Designed to be extensible to other domains beyond travel/weather.
  - Configurable embedding store and LLM backends, and modular vector DB interface to swap implementations.

- Basic robustness:
  - Error handling and user-facing messages when API keys or data files are missing.
  - Clear messages guiding setup (required data files and env keys).
