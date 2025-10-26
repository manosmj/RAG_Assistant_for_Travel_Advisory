# 🌍 RAG-Based Travel Advisory Assistant

A Retrieval-Augmented Generation (RAG) chatbot for travel advisory information, powered by ChromaDB, Sentence Transformers, and advanced LLM technology. Get accurate and contextual answers about travel advisories, safety information, and destination guidelines.

---

## 🚀 Technologies Used

- **Python 3.8+**
- **ChromaDB** — Vector database for document retrieval
- **Sentence Transformers** — Text embedding (all-MiniLM-L6-v2)
- **Large Language Model** — For natural language understanding and generation
- **LangChain** — Text chunking and metadata management
- **OpenWeather API** — Real-time weather data retrieval

---

## 🧠 Key Features

- **Weather-Specific Travel Advisory:**
  - Real-time weather data access for any country
  - Weather analysis through LLM integration
  - Structured weather data processing

- **RAG Implementation:**
  - Embeds and stores travel advisory documents in ChromaDB
  - Retrieves relevant context for user queries
  - Augments LLM prompt with retrieved context

- **Data Processing:**
  - Advanced semantic embedding using Sentence Transformers
  - Secure API key management
  - Efficient document chunking and metadata handling

---

## 📦 Project Structure

```
RAG_Assistant_for_Travel_Advisory/
├── vectordb.py          # Collect, Chunk and Store Weather data
├── weather_app.py       # Weather-focused advisory implementation
├── weather_forecast.py  # Forecast weather using Open Weather API
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── chroma_db/           # ChromaDB persistent storage
│   └── ...
├── data/               
│   ├── weather/         # Weather data files
└── .gitignore           # Excludes .env, venv, etc.
```

---

## ⚡️ How to Run

### 1. Clone the repository
```sh
git clone https://github.com/manosmj/RAG_Assistant_for_Travel_Advisory.git
cd RAG_Assistant_for_Travel_Advisory
```

### 2. Set up a Python environment
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# Or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure API Keys
Set up your API keys as environment variables:
```sh
# For OpenWeather API
export OPENWEATHER_API_KEY="your-openweather-api-key"
# For LLM Service
export GROQ_API_KEY="your-groq-api-key"
or
export GOOGLE_API_KEY="your-google-api-key"
or
export OPEN_API_KEY="your-open-api-key"
```

### 5. Prepare Data
- Ensure weather data files are in `data/weather/`

### 6. Launch the Application
```sh
python src/weather_forecast.py
python src/weather_app.py
```

---

## 🔒 Security Notes
- **Never commit API keys or .env files to GitHub**
- Keep sensitive configuration in environment variables
- Regular security audits recommended

---

## 📝 Usage
- Enter a country name to get weather information
- View weather analysis and travel recommendations
- Access historical weather patterns and travel advisories

---

## 📚 References
- [ChromaDB Documentation](https://www.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenWeather API](https://openweathermap.org/api)
- [LangChain](https://langchain.org/)

---

## 👤 Author
- [manosmj](https://github.com/manosmj)

---

## 🔒 License
This project is licensed under the MIT License.

---
