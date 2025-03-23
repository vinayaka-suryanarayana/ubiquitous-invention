import requests
import argparse

API_KEY = "your_api_key_here"

url_city = "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={api_key}"
url_zip = "http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}"

class CityData:
    def __init__(self, name, lat, lon, country):
        """
        Initialize a CityData object.

        :param name: Name of the city.
        :param lat: Latitude of the city.
        :param lon: Longitude of the city.
        :param country: Country code of the city.
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.country = country

    def __repr__(self):
        return f"CityData(\n\tname={self.name}, \n\tlat={self.lat}, \n\tlon={self.lon}, \n\tcountry={self.country}\n\t)"

def get_city_data(city, state, country="US", limit=1, api_key=API_KEY):
    """
    Fetch city data from OpenWeatherMap API based on city and state.

    :param city: The name of the city.
    :param state: The state code.
    :param country: The country code (default is "US").
    :param limit: The maximum number of results to return (default is 1).
    :param api_key: The API key for authentication (default is the global API_KEY).
    :return: A CityData object containing city information or None if not found.
    """
    formatted_url = url_city.format(city_name=city, state_code=state, country_code=country, limit=limit, api_key=api_key)
    response = requests.get(formatted_url)
    data = response.json()

    # Check if the response contains any locations
    if isinstance(data, list) and len(data) > 0:
        # Return a CityData object
        return CityData(
            name=data[0]['name'],
            lat=data[0]['lat'],
            lon=data[0]['lon'],
            country=data[0]['country']
        )
    return None  # Return None if no locations are found

def get_city_data_by_zip(zip_code, country="US", api_key=API_KEY):
    """
    Fetch city data from OpenWeatherMap API based on zip code.

    :param zip_code: The zip code of the location.
    :param country: The country code (default is "US").
    :param api_key: The API key for authentication (default is the global API_KEY).
    :return: A CityData object containing city information or None if not found.
    """
    formatted_url = url_zip.format(zip_code=zip_code, country_code=country, api_key=api_key)
    response = requests.get(formatted_url)
    data = response.json()
    
    # Check if the response contains any locations
    if isinstance(data, dict) and 'name' in data:  # Check if data is a dictionary and contains 'name'
        # Return a CityData object
        return CityData(
            name=data['name'],
            lat=data['lat'],
            lon=data['lon'],
            country=data['country']
        )
    return None  # Return None if no locations are found

def fetch_city_data_for_locations(locations):
    """
    Fetch city data for a list of locations, which can be city/state or zip code.

    :param locations: A list of locations in the format "City, State" or "Zip Code".
    :return: A list of CityData objects for the valid locations.
    """
    city_data_list = []  
    for location in locations:
        # Check if the input is a zip code or a city/state
        if location.isdigit() and len(location) == 5:  # Assuming US zip codes are 5 digits
            data = get_city_data_by_zip(location)
            if data:
                city_data_list.append(data)  
            else:
                print(f"No weather data found for zip code {location}.")
        else:
            # Split the location into city and state
            parts = location.split(",")
            if len(parts) == 2:
                city = parts[0].strip()
                state = parts[1].strip()
                data = get_city_data(city, state)
                if data:
                    city_data_list.append(data)  
                else:
                    print(f"No weather data found for {location}.")
            else:
                print(f"Invalid location format: {location}")
    
    return city_data_list  # Return the list of CityData objects

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather data for specified locations.")
    parser.add_argument("--locations", nargs='+', help='List of locations in the format "City, State" or "Zip Code"', required=True)
    args = parser.parse_args()
    
    city_data = fetch_city_data_for_locations(args.locations)
    for data in city_data:
        print(data)  # Print each CityData object





