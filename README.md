
# 🤖 RAG-Based Travel Assistant

This application is a user-friendly tool for obtaining real-time weather data and relevant travel advice for any country in the world. By simply entering a country name, users can instantly access key weather metrics and receive curated tips to help them plan their trip effectively. This app leverages Open Weather API to provide accurate, up-to-date information, making it a convenient resource for travelers, students, or anyone interested in global weather patterns.

## Features:

- RAG (Retrieval-Augmented Generation) travel assistant core:
  - Retrieval + generation pipeline that searches a vector DB for relevant context and uses an LLM to generate answers.
  - Combines retrieved chunks into context and runs a prompt → LLM → output parser chain.
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

