from pathlib import Path
from datetime import datetime
import os

def get_weather_data(country: str) -> dict:
    """Read weather data from the country's weather file"""
    weather_file = Path(__file__).parent.parent / "data" / "weather" / f"{country.lower()}_weather.txt"
    
    if not weather_file.exists():
        return None
        
    weather_data = {}
    with open(weather_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                weather_data[key.strip()] = value.strip()
    
    return weather_data

def generate_travel_advisory(country: str) -> str:
    """Generate weather-based travel advisory for the country"""
    
    weather_data = get_weather_data(country)
    if not weather_data:
        return f"No weather data available for {country}"

    # Create travel advisory based on weather conditions
    temp = float(weather_data.get('Temperature', '0').replace('°C', ''))
    humidity = int(weather_data.get('Humidity', '0').replace('%', ''))
    weather = weather_data.get('Weather', '').lower()
    
    # Weather-based recommendations
    clothing = []
    activities = []
    precautions = []
    
    # Temperature based advice
    if temp > 30:
        clothing.extend(['light cotton clothes', 'sun hat', 'sunglasses'])
        activities.extend(['indoor activities during peak hours', 'early morning sightseeing'])
        precautions.append('stay hydrated')
    elif temp < 15:
        clothing.extend(['warm jacket', 'layers', 'thermal wear'])
        activities.extend(['outdoor activities during sunny hours'])
        precautions.append('carry warm beverages')
    
    # Weather condition based advice
    if 'rain' in weather:
        clothing.append('raincoat/umbrella')
        activities.append('indoor cultural activities')
        precautions.append('check local weather updates')
    elif 'clear' in weather:
        activities.extend(['outdoor sightseeing', 'photography'])
    
    # Humidity based advice
    if humidity > 70:
        precautions.append('carry personal fan/cooling items')
        clothing.append('moisture-wicking fabrics')

    advisory = f"""
🌍 Travel Advisory for {country}

Current Weather Conditions:
-------------------------
📍 Location: {weather_data.get('Location', 'Not specified')}
🌡️ Temperature: {weather_data.get('Temperature', 'N/A')}
🌤️ Weather: {weather_data.get('Weather', 'N/A')}
💨 Wind Speed: {weather_data.get('Wind Speed', 'N/A')}
💧 Humidity: {weather_data.get('Humidity', 'N/A')}

Travel Recommendations:
---------------------
👔 Suggested Clothing: {', '.join(clothing)}

🎯 Recommended Activities: {', '.join(activities)}

⚠️ Precautions: {', '.join(precautions)}

🕒 Weather data last updated: {weather_data.get('Generated on', 'Not specified')}

Note: This is a general advisory based on current weather conditions. Please check local forecasts and travel guidelines before making plans.
"""
    return advisory

def main():
    country = input("Enter country name: ")
    advisory = generate_travel_advisory(country)
    print(advisory)

if __name__ == "__main__":
    main()