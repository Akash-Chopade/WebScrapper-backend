import requests
from bs4 import BeautifulSoup
import datetime

def get_weather_data(city):
    """
    Scrape weather data for a given city from Times of India
    Returns a dictionary with weather information or None if error occurs
    """
    try:
        url = f'https://timesofindia.indiatimes.com/travel/{city}/weather'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        # Check for 404 or invalid city
        if r.status_code == 404:
            return {
                'status': 'error',
                'message': f'City "{city}" not found. Please check the spelling and try again.',
                'error_type': 'city_not_found'
            }
        
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        # Extract weather data
        temp = soup.find('span', attrs={'class': "tempdigitbox"})
        date = soup.find('span', attrs={'class': "date-time"})
        humidity = soup.find('strong', attrs={'data-weather': "max-humid"})
        wind = soup.find('strong', attrs={'data-weather': "wind-spd"})
        rain = soup.find('strong', attrs={'data-weather': "rain-prob"})
        min_max = soup.find('div', attrs={'class': "sunrise_set"})
        city_name = soup.find('h3')
        environment = soup.find('span', attrs={'class': "tempimg"})

        # Prepare response data
        weather_data = {
            'city': city_name.text.strip() if city_name else city.title(),
            'date': datetime.datetime.today().strftime('%a, %B %d'),
            'time': datetime.datetime.today().strftime('%I:%M %p'),
            'temperature': temp.text.strip() if temp else "Temperature not available",
            'environment': environment.text.strip() if environment else "Environment info not available",
            'humidity': humidity.text.strip() if humidity else "N/A",
            'wind_speed': f"{wind.text.strip()} kmph" if wind else "N/A",
            'rain_probability': f"{rain.text.strip()}%" if rain else "N/A",
            'status': 'success'
        }
        
        # Check if we got valid data
        if not temp or temp.text.strip() == "":
            return {
                'status': 'error',
                'message': f'Weather data not available for "{city}". Please try another city.',
                'error_type': 'no_data_found'
            }
        
        return weather_data
        
    except requests.RequestException as e:
        if "404" in str(e):
            return {
                'status': 'error',
                'message': f'City "{city}" not found. Please check the spelling and try again.',
                'error_type': 'city_not_found'
            }
        return {
            'status': 'error',
            'message': f'Network error: Unable to fetch weather data. Please check your internet connection.',
            'error_type': 'network_error'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }

def print_weather_cli(city):
    """
    Print weather data in CLI format (original functionality)
    """
    print('Searching....')
    weather_data = get_weather_data(city)
    
    if weather_data['status'] == 'success':
        print()
        print(weather_data['city'])
        print(f"{weather_data['date']}  {weather_data['time']}")
        print()
        print(weather_data['temperature'])
        print(weather_data['environment'])
        print()
        print(f"Humidity : {weather_data['humidity']}")
        print(f"Wind Speed : {weather_data['wind_speed']}")
        print(f"Rain Probability : {weather_data['rain_probability']}\n\n")
    else:
        print(weather_data['message'])

if __name__ == "__main__":
    # CLI mode - original functionality
    city = input('Enter city from India : ')
    print_weather_cli(city)
