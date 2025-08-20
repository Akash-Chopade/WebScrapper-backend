from flask import Flask, jsonify, request
from flask_cors import CORS
from weather_scraper import get_weather_data
import os

# Indian cities for autocomplete suggestions
INDIAN_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Surat',
    'Pune', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal',
    'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana',
    'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar',
    'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Navi Mumbai', 'Allahabad',
    'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur',
    'Madurai', 'Raipur', 'Kota', 'Guwahati', 'Chandigarh', 'Solapur', 'Hubli-Dharwad',
    'Tiruchirappalli', 'Bareilly', 'Mysore', 'Tiruppur', 'Gurgaon', 'Aligarh', 'Jalandhar',
    'Bhubaneswar', 'Salem', 'Mira-Bhayandar', 'Warangal', 'Thiruvananthapuram', 'Guntur',
    'Bhiwandi', 'Saharanpur', 'Gorakhpur', 'Bikaner', 'Amravati', 'Noida', 'Jamshedpur',
    'Bhilai', 'Cuttack', 'Firozabad', 'Kochi', 'Nellore', 'Bhavnagar', 'Dehradun',
    'Durgapur', 'Asansol', 'Rourkela', 'Nanded', 'Kolhapur', 'Ajmer', 'Akola', 'Gulbarga',
    'Jamnagar', 'Ujjain', 'Loni', 'Siliguri', 'Jhansi', 'Ulhasnagar', 'Jammu', 'Sangli-Miraj',
    'Mangalore', 'Erode', 'Belgaum', 'Ambattur', 'Tirunelveli', 'Malegaon', 'Gaya',
    'Jalgaon', 'Udaipur', 'Maheshtala'
]

app = Flask(__name__)

# Configure CORS - Allow all origins for now
# You can restrict this later to your specific frontend domain
CORS(app, origins="*")

@app.route('/')
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Weather Scraper API',
        'version': '1.0.0',
        'endpoints': {
            '/api/weather/<city>': 'GET - Get weather data for a specific city',
            '/api/cities/search': 'GET - Search for city suggestions'
        }
    })

@app.route('/api/weather/<city>', methods=['GET'])
def get_weather(city):
    """Get weather data for a specific city"""
    if not city or len(city.strip()) == 0:
        return jsonify({
            'status': 'error',
            'message': 'City name is required'
        }), 400
    
    # Clean city name
    city = city.strip().lower()
    
    # Get weather data
    weather_data = get_weather_data(city)
    
    if weather_data['status'] == 'error':
        # Return appropriate HTTP status codes based on error type
        if weather_data.get('error_type') == 'city_not_found':
            return jsonify(weather_data), 404
        elif weather_data.get('error_type') == 'no_data_found':
            return jsonify(weather_data), 404
        else:
            return jsonify(weather_data), 500
    
    return jsonify(weather_data)

@app.route('/api/cities/search', methods=['GET'])
def search_cities():
    """Search for city suggestions based on query"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Query parameter "q" is required'
        }), 400
    
    # Filter cities that match the query
    suggestions = [city for city in INDIAN_CITIES if query in city.lower()]
    
    # Limit to top 10 suggestions
    suggestions = suggestions[:10]
    
    return jsonify({
        'status': 'success',
        'suggestions': suggestions,
        'query': query
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'weather-scraper-api'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
