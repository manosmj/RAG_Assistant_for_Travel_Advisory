import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

class WeatherForecast:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("Please set OPENWEATHER_API_KEY in .env file")
        
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.data_dir = Path(__file__).parent.parent / "data" / "weather"
        self.geolocator = Nominatim(user_agent="weather_forecast")
        
        # Create weather data directory
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_coordinates(self, location: str) -> tuple:
        """Get latitude and longitude for a location."""
        try:
            # Special handling for Canada
            if location.lower() == "canada":
                # Using Ottawa (capital) coordinates as default for Canada
                return 45.4215, -75.6972
            
            # Special handling for Brazil
            if location.lower() == "brazil":
                # Using Brasilia (capital) coordinates as default for Brazil
                return -15.7801, -47.9292
            
            # Special handling for Niger
            if location.lower() == "niger":
                # Using Niamey (capital) coordinates as default for Niger
                return 13.5137, 2.1098

            # Special handling for Palau
            if location.lower() == "palau":
                # Using Ngerulmud (capital) coordinates as default for Palau
                return 7.5000, 134.6241

            loc = self.geolocator.geocode(location, timeout=10)
            if loc:
                print(f"Found coordinates for {location}: {loc.latitude}, {loc.longitude}")
                return loc.latitude, loc.longitude
            
            print(f"Could not find coordinates for {location}")
            return None
        except Exception as e:
            print(f"Error getting coordinates for {location}: {e}")
            return None

    def get_weather(self, lat: float, lon: float) -> Dict:
        """Fetch weather data for given coordinates."""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'  # For Celsius
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def format_weather_data(self, weather_data: Dict) -> str:
        """Format weather data into readable text."""
        if not weather_data:
            return "No weather data available"

        return f"""Weather Forecast
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Location: {weather_data['name']}, {weather_data['sys']['country']}
Temperature: {weather_data['main']['temp']}°C
Feels Like: {weather_data['main']['feels_like']}°C
Humidity: {weather_data['main']['humidity']}%
Weather: {weather_data['weather'][0]['description']}
Wind Speed: {weather_data['wind']['speed']} m/s
"""

    def save_forecast(self, country: str, weather_data: str):
        """Save weather forecast to a text file."""
        file_path = self.data_dir / f"{country.lower()}_weather.txt"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(weather_data)
            print(f"Saved forecast for {country}")
        except Exception as e:
            print(f"Error saving forecast for {country}: {e}")

    def update_all_forecasts(self, countries: List[str]):
        """Update weather forecasts for all specified countries."""
        for country in countries:
            print(f"\nProcessing {country}...")
            coords = self.get_coordinates(country)
            if coords:
                weather_data = self.get_weather(*coords)
                if weather_data:
                    formatted_data = self.format_weather_data(weather_data)
                    self.save_forecast(country, formatted_data)
            else:
                print(f"Could not find coordinates for {country}")

def main():
    # List of countries to fetch weather for
    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
        "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
        "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
        "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", 
        "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", 
        "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", 
        "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", 
        "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", 
        "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", 
        "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", 
        "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", 
        "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
        "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", 
        "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", 
        "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", 
        "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", 
        "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", 
        "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", 
        "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
        "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", 
        "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", 
        "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
        "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", 
        "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", 
        "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", 
        "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", 
        "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", 
        "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
    ]

    try:
        weather_service = WeatherForecast()
        weather_service.update_all_forecasts(countries)
        print("\nWeather forecast update completed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()